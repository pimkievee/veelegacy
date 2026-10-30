#!/usr/bin/env python3
"""Check curated application links without scraping or republishing job text.

403/429/5xx and network errors remain unknown, never closed. Status is public
job metadata only. The page also enforces explicit closing timestamps.
"""
import concurrent.futures
import datetime as dt
import json
import pathlib
import re
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]

def extract_jobs(source):
    decoder = json.JSONDecoder()
    jobs = []
    for match in re.finditer(r"const\s+\w+\s*=\s*(?=\[\{)", source):
        try:
            values, _ = decoder.raw_decode(source[match.end():])
            jobs.extend(j for j in values if isinstance(j, dict) and j.get('title') and j.get('company'))
        except ValueError:
            continue
    return jobs

def classify(code, final_url, body):
    if code in (404, 410):
        return 'closed'
    if code != 200:
        return 'unknown'
    if 'error=true' in final_url and 'greenhouse.io' in final_url:
        return 'closed'
    # Match explicit page notices, not generic hiring or privacy boilerplate.
    if re.search(r"(?:the job you are trying to apply for has been filled|this job is no longer available|this position is no longer accepting applications)", body, re.I):
        return 'closed'
    return 'reachable'

def check(job, now):
    url = job['url']
    stamp = now.isoformat().replace('+00:00', 'Z')
    expiry = job.get('expires_at')
    if expiry:
        try:
            if dt.datetime.fromisoformat(expiry.replace('Z', '+00:00')) <= now:
                return url, {'status':'closed','checked_at':stamp,'reason':'closing_date'}
        except ValueError:
            pass
    try:
        request = urllib.request.Request(url, headers={'User-Agent':'VeeLegacyCareerHub-LinkCheck/1.0'})
        with urllib.request.urlopen(request, timeout=12) as response:
            body = response.read(250000).decode('utf-8', errors='replace')
            status = classify(response.status, response.url, body)
            return url, {'status':status,'checked_at':stamp}
    except urllib.error.HTTPError as error:
        return url, {'status':classify(error.code, url, ''),'checked_at':stamp}
    except (OSError, TimeoutError):
        return url, {'status':'unknown','checked_at':stamp}

def main():
    now = dt.datetime.now(dt.timezone.utc)
    jobs = extract_jobs((ROOT/'jobs/index.html').read_text())
    jobs.extend(json.loads((ROOT/'jobs/jobs.json').read_text()))
    urls = {j['url']:j for j in jobs if isinstance(j.get('url'), str) and j['url'].startswith('https://')}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = dict(pool.map(lambda j:check(j,now), urls.values()))
    output = {'updated_at':now.isoformat().replace('+00:00','Z'),'jobs':results}
    (ROOT/'jobs/job-status.json').write_text(json.dumps(output, indent=2)+'\n')
    print('Checked',len(results),'job links;',sum(v['status']=='closed' for v in results.values()),'closed')

if __name__ == '__main__':
    main()
