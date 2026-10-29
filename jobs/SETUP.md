# VeeLegacy Career Hub — automated job feed setup

## Current state
The landing page is on the development branch. No employer feeds are activated and no jobs have been imported. No live site deployment has been made.

## How automation works
1. Review each employer's job-board API terms and obtain explicit authorization to republish job titles, summaries and links where required.
2. Add each approved employer to `jobs/sources.json` with `id`, `company`, `provider` (`greenhouse` or `lever`), `board_token`, `region` and `approved_for_republication: true`.
3. Run `python3 scripts/update_jobs.py` locally to validate the data.
4. Review output and publish via pull request.
5. GitHub Actions can schedule daily updates after the workflow exists on the repository default branch. The workflow currently targets the development branch; adjust the checkout and push refs when publishing.

Example source entry (placeholder only, not an approved feed):
```json
{"id":"example-employer","company":"Example Employer","provider":"greenhouse","board_token":"example","region":"Canada","approved_for_republication":false}
```

## Important limitations
- Public API availability does not establish redistribution rights.
- International applicant eligibility, sponsorship, LMIA, work authorization, and remote-worldwide status are always unconfirmed unless a verified source explicitly states otherwise.
- No scraping, no paid job postings copied without permission, and no fabricated listings.
- Daily workflows are best-effort, not guaranteed to run at an exact minute.
- The site is static; email subscriptions and ad monetization require additional services and compliance setup.
- A failed feed preserves existing data; plan to add freshness timestamps and expiration checks before public launch.
