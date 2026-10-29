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

def text(value):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", str(value or "")))).strip()[:500]

def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "VeeLegacyCareerHub/1.0 (job feed integration)"})
    with urllib.request.urlopen(request, timeout=20) as response:
        if response.status != 200:
            raise ValueError("Unexpected HTTP status")
        return json.load(response)

def normalize(raw, source):
    title = text(raw.get("title") or raw.get("text"))
    company = text(source["company"])
    url = raw.get("absolute_url") or raw.get("hostedUrl") or raw.get("applyUrl")
    if not isinstance(url, str) or urllib.parse.urlparse(url).scheme != "https":
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
    # Never infer visa sponsorship, LMIA, work authorization, or worldwide eligibility.
    return {"id": source["id"] + ":" + str(raw.get("id") or raw.get("text") or url),
            "title": title, "company": company, "location": location,
            "region": source.get("region", "Canada"), "category": category,
            "eligibility": "unknown", "eligibilityLabel": "Eligibility not confirmed",
            "url": url, "source": source["id"]}

def main():
    config = json.loads(SOURCES.read_text(encoding="utf-8"))
    sources = config.get("sources", [])
    if not sources:
        print("No approved sources configured; preserving existing job data.")
        return 0
    collected = {}
    failed = []
    for source in sources:
        if not source.get("approved_for_republication"):
            continue
        try:
            provider = source["provider"]
            token = urllib.parse.quote(source["board_token"], safe="")
            if provider == "greenhouse":
                data = fetch("https://boards-api.greenhouse.io/v1/boards/" + token + "/jobs")
                entries = data["jobs"]
            elif provider == "lever":
                data = fetch("https://api.lever.co/v0/postings/" + token + "?mode=json")
                entries = data
            else:
                raise ValueError("Unsupported provider")
            if not isinstance(entries, list):
                raise ValueError("Unexpected feed response")
            for raw in entries[:MAX_PER_SOURCE]:
                item = normalize(raw, source)
                if item:
                    collected[item["url"]] = item
            print("Imported", source["id"], len(entries))
        except (KeyError, ValueError, OSError, TimeoutError, json.JSONDecodeError) as error:
            failed.append(source.get("id", "unknown"))
            print("Feed failed:", source.get("id"), type(error).__name__, file=sys.stderr)
    # Avoid deleting known listings when a feed is temporarily unavailable.
    if failed:
        print("Import incomplete; keeping existing dataset unchanged.", file=sys.stderr)
        return 1
    # Only replace if at least one approved feed completed; empty is valid if feeds have no jobs.
    if any(s.get("approved_for_republication") for s in sources):
        OUTPUT.write_text(json.dumps(sorted(collected.values(), key=lambda x:(x["company"],x["title"])), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("Published", len(collected), "verified-source listings")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
