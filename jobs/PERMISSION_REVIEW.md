# First employer-feed verification register

Reviewed: 2026-10-29

| Provider | Technical API access | Third-party commercial republication approval | Decision |
| --- | --- | --- | --- |
| Greenhouse Job Board API | Public GET endpoints for company boards | Not established for VeeLegacy's independent multi-employer aggregator | Pending employer authorization |
| Lever Postings API | Public published-posting endpoint for individual companies | Not established for VeeLegacy's independent multi-employer aggregator | Pending employer authorization |

## Primary sources
- Greenhouse official Job Board API: https://docs.greenhouse.io/job-board
- Greenhouse official API overview: https://support.greenhouse.io/hc/en-us/articles/10568627186203-Greenhouse-API-overview
- Lever official Postings API: https://github.com/lever/postings-api
- Lever official developer support: https://hire.lever.co/developer/support

## Next authorization actions
1. Identify 3-5 target employers with an active official Greenhouse or Lever careers page.
2. Contact the employer's recruiting/careers web team (or platform partner channel) to request written permission for VeeLegacy Career Hub to display job title, employer, location, and direct apply link; ask about commercial monetization, attribution, caching, update frequency, and takedown requests.
3. Record their reply or licensing terms in a permission reference.
4. Only then add the corresponding board token to sources.json and set approved_for_republication=true.
5. Validate live imports, job freshness, and job-link redirects in a development run before publishing.

No employers have yet granted approval. No feed is enabled.
