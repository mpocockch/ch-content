# WhatConverts webhook relay

Starts the sync workflow the moment a rep marks a call quotable, instead of
waiting for GitHub's schedule.

The scheduled run is not a reliable clock. Measured over 9 weekdays it fired 35
of 234 requested slots -- about 15% -- at a median gap of 3.2 hours. One real
lead took 4 hours to reach HubSpot. The schedule stays in place as a safety net,
but it cannot be the path a sales callback depends on.

WhatConverts cannot send a custom `Authorization` header, and GitHub's API
requires one, so the two cannot be wired together directly. This relay is the
adapter: about 20 lines, deployed on Cloudflare Workers' free tier.

**If the WhatConverts webhook form does offer custom headers, skip this
directory entirely** -- point the webhook straight at GitHub's dispatch endpoint
with an `Authorization: Bearer <token>` header and the same JSON body the worker
sends. The relay exists only to supply a header WhatConverts probably cannot.

## What it does, and does not, trust

The relay ignores the request body. WhatConverts cannot sign its webhooks, so
nothing in the payload is trustworthy. The POST is treated as "something
changed, go look"; the sync then reads the WhatConverts API itself and applies
the same `quotable` verification and dedup checks as always.

The consequence is that a forged request is harmless: it starts a run that finds
nothing to do. The secret in the URL path keeps out background internet noise,
but it is a bearer token in a URL, not real authentication, and the design does
not rely on it.

## Deploy

### 1. GitHub token

A fine-grained personal access token, scoped to `mpocockch/ch-content` only,
with **Actions: read and write**. That permission lets it start this workflow
and nothing else -- no repository contents, no secrets.

### 2. Worker

At [dash.cloudflare.com](https://dash.cloudflare.com) -> Workers & Pages ->
Create -> Worker. Paste `worker.js`, deploy, then add two secrets under
Settings -> Variables and Secrets:

| Secret | Value |
| --- | --- |
| `GITHUB_TOKEN` | the token from step 1 |
| `RELAY_PATH` | a long random string, e.g. `openssl rand -hex 24` |

Your webhook URL is `https://<worker>.workers.dev/<RELAY_PATH>`. Any other path
returns 404.

### 3. WhatConverts webhook

Tracking -> Integrations -> Automations -> Webhooks -> Add Webhook. Paste the
URL and enable **Phone Calls (modified)** -- marking a call quotable is a
modification to an existing lead, not a new one, so the "new lead" trigger alone
would never fire for this.

### 4. Check it

Mark a call quotable in WhatConverts. A run should appear in the Actions tab
within seconds, its banner reading `LIVE RUN`, not `DRY RUN`.

## Cost and volume

The "modified" trigger fires on *any* edit to a phone-call lead, not only a
change to `quotable`. At current volume that is a handful of extra runs a day,
each about 20 seconds, which is immaterial against the Actions allowance. If the
runs ever get noisy, the relay can read `quotable` from the payload and skip the
dispatch when it is not `Yes` -- as an efficiency filter only, never as a
correctness check, with the scheduled sweep covering anything wrongly skipped.
