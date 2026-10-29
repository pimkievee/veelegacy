#!/usr/bin/env python3
"""Import permitted employer job feeds into the VeeLegacy Career Hub.

No sources are enabled by default. Configure jobs/sources.json only after
confirming permission to republish job summaries and external application links.
"""
import datetime as dt
import html
import json
import pathlib
import re
import sys
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCES = ROOT / "jobs" / "sources.json"
OUTPUT = ROOT / "jobs" / "jobs.json"
MAX_PER_SOURCE = 200
MAX_STALE_DAYS = 3

def text(value):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", str(value or "")))).strip()[:500]

def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "VeeLegacyCareerHub/1.0 (job feed integration)"})
    with urllib.request.urlopen(request, timeout=20) as response:
        if response.status != 200:
            raise ValueError("Unexpected HTTP status")
        return json.load(response)

def normalize(raw, source, checked_at=None):
    title = text(raw.get("title") or raw.get("text"))
    company = text(source["company"])
    url = raw.get("absolute_url") or raw.get("hostedUrl") or raw.get("applyUrl")
    if not isinstance(url, str) or urllib.parse.urlparse(url).scheme != "https" or not urllib.parse.urlparse(url).hostname:
        return None
    location = raw.get("location") or raw.get("categories", {}).get("location")
    if isinstance(location, dict):
        location = location.get("name")
    location = text(location) or "Location not specified"
    if not title:
        return None
    haystack = (title + " " + location).lower()
    category = "Other"
    for name, terms in [
        ("Healthcare", ["nurse", "caregiver", "psw", "personal support", "health", "medical"]),
        ("Social Services", ["social work", "social service", "case worker", "youth worker", "counsellor"]),
        ("Technology", ["engineer", "developer", "devops", "software", "data analyst", "security"]),
        ("Government", ["public service", "government", "policy analyst"]),
        ("Skilled Trades", ["electrician", "plumber", "mechanic", "construction"]),
    ]:
        if any(term in haystack for term in terms):
            category = name
            break
    checked_at = checked_at or dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")
    # Never infer visa sponsorship, LMIA, work authorization, or worldwide eligibility.
    return {"id": source["id"] + ":" + str(raw.get("id") or raw.get("text") or url),
            "title": title, "company": company, "location": location,
            "region": source.get("region", "Canada"), "category": category,
            "eligibility": "unknown", "eligibilityLabel": "Eligibility not confirmed",
            "url": url, "source": source["id"], "last_seen_at": checked_at}

def parse_time(value):
    if not isinstance(value, str):
        return None
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.astimezone(dt.timezone.utc) if parsed.tzinfo else None
    except ValueError:
        return None

def fresh(job, now):
    seen = parse_time(job.get("last_seen_at"))
    if not seen or seen > now + dt.timedelta(minutes=5):
        return False
    if now - seen > dt.timedelta(days=MAX_STALE_DAYS):
        return False
    expires = parse_time(job.get("expires_at"))
    return expires is None or expires > now

def read_existing():
    try:
        data = json.loads(OUTPUT.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (OSError, ValueError):
        return []

def save(jobs):
    OUTPUT.write_text(json.dumps(sorted(jobs, key=lambda x: (x.get("company", ""), x.get("title", ""))), ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")

def main():
    now = dt.datetime.now(dt.timezone.utc)
    config = json.loads(SOURCES.read_text(encoding="utf-8"))
    approved = [s for s in config.get("sources", []) if s.get("approved_for_republication")]
    for source in approved:
        if not all(source.get(field) for field in ("id", "company", "provider", "board_token", "permission_reference")):
            print("Approved source missing required details or permission reference.", file=sys.stderr)
            return 1
        if source["provider"] not in ("greenhouse", "lever"):
            print("Unsupported approved source provider.", file=sys.stderr)
            return 1
    if not approved:
        if read_existing():
            save([])
        print("No approved sources; zero listings published.")
        return 0
    collected = {}
    failed = []
    checked_at = now.isoformat().replace("+00:00", "Z")
    for source in approved:
        try:
            token = urllib.parse.quote(source["board_token"], safe="")
            if source["provider"] == "greenhouse":
                entries = fetch("https://boards-api.greenhouse.io/v1/boards/" + token + "/jobs")["jobs"]
            else:
                entries = fetch("https://api.lever.co/v0/postings/" + token + "?mode=json")
            if not isinstance(entries, list) or len(entries) > MAX_PER_SOURCE:
                raise ValueError("Invalid or truncated feed")
            for raw in entries:
                item = normalize(raw, source, checked_at=checked_at)
                if item:
                    collected[item["url"]] = item
            print("Imported", source["id"], len(entries))
        except (KeyError, ValueError, OSError, TimeoutError, json.JSONDecodeError, TypeError) as error:
            failed.append(source["id"])
            print("Feed failed:", source["id"], type(error).__name__, file=sys.stderr)
    # Successful feeds replace their previous listings, automatically removing closed jobs.
    # Failed feeds retain only recently confirmed listings, never indefinitely.
    failed_ids = set(failed)
    for job in read_existing():
        if (isinstance(job, dict) and job.get("source") in failed_ids and fresh(job, now)
                and isinstance(job.get("url"), str) and job["url"] not in collected):
            collected[job["url"]] = job
    save([job for job in collected.values() if fresh(job, now)])
    print("Published", len(collected), "candidate jobs; failed feeds:", len(failed))
    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main())
