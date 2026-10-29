# Employer feed onboarding checklist

The Career Hub must not automatically redistribute job postings just because an API is public.

## Initial providers to assess
- Greenhouse Job Board API — employer-specific public board token; request/verify redistribution permission.
- Lever Postings API — employer-specific public site identifier; request/verify redistribution permission.
- Canada Job Bank — pursue the official job-board feed partnership only after eligibility requirements are satisfied.

## Approval checklist for every employer
1. Identify employer, official careers page and job board provider.
2. Record the exact terms or written authorization that allows third-party commercial republishing of job title, employer, location, and outbound application link.
3. Record a URL or permission ticket in `permission_reference`.
4. Confirm permitted attribution and any caching, retention, or deletion requirements.
5. Check the board token and test with a small sample before enabling.
6. Set `approved_for_republication: true` only after approval.
7. Never infer LMIA, visa sponsorship, work authorization or remote-worldwide eligibility from job title/location.
8. Review job freshness and expiration handling before public launch.

## Example entry (not active)
```json
{
  "id": "sample-employer",
  "company": "Sample Employer",
  "provider": "greenhouse",
  "board_token": "sample-employer",
  "region": "Canada",
  "approved_for_republication": false,
  "permission_reference": ""
}
```

## Operations
The scheduled GitHub Actions workflow only becomes active when registered on the repository default branch. It currently checks out and writes to the development branch, and should not be merged unchanged without reviewing branch targets. API access and publishing permissions are separate issues. Do not list any employer as a partner without their approval.
