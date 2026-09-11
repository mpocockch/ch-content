# Blog Content Pipeline — Playbook

The single source of truth for how a C&H Electric blog post gets from an idea in Teams to a
live page on chelectric.com. Every scheduled Routine starts by reading this file.

**Owners:** Matt Pocock, Bill Concannon

**Cadence target: 2–3 blog posts per month.** Settled by Matt 2026-09-11. Note that
`C&H Electric Blog Strategy.docx` says 8–10 posts per month — that figure refers to **social
posts, not blog articles**, and does not apply here. Do not "correct" the cadence upward from
that document.

Drafting runs weekly on Friday, which gives headroom above the target: if no topic is approved
the run stops cleanly, and that is the throttle working, not a failure. Promotion into
`Approved Ideas` at the Thursday triage (§9) is what actually sets volume — roughly one
promotion a fortnight sustains the target.

---

## 1. Design rules

These exist because the previous build broke. Do not undo them without reading why.

1. **Every Routine runs in a fresh session.** No Routine may be bound to a persistent
   session. Two Routines were previously bound to one chat session created 2026-07-29; by
   September it held 105k tokens of context before a run even began, and it eventually
   wedged with a stuck tool call. Every firing after that landed in a dead conversation and
   still reported `SUCCEEDED`, because for a session-bound Routine "succeeded" only means
   the wake message was delivered.
2. **State lives in this repo and on the Asana card. Never in conversation.** A run may
   assume nothing about what previous runs "know."
3. **Asana is the state machine.** A card's section *is* its stage. Read stage from Asana at
   the start of every run; never infer it.
4. **Git is the durable store. SharePoint and Word are only the review surface.** Commit the
   draft and the hero image *before* attempting any upload. A failed upload must cost a
   retry, never the work.
5. **One Routine, one job, minimum connectors.** A broken connector should stall one stage,
   not the pipeline.
6. **A blocked run must be loud.** Push and email notifications are on for every Routine. A
   silent skip is the failure mode this whole design exists to prevent.

---

## 2. Stage map

| # | Stage | Actor | System |
|---|---|---|---|
| 01 | Idea posted | **Human** — anyone | Teams `Blog Ideas` |
| 02 | Idea captured to `Unapproved Ideas` | Agent | Teams → Asana |
| 03 | Topic promoted to `Approved Ideas` | **Human** — reviewer | Asana |
| 04 | Draft written | Agent | Repo (`drafts/`) |
| 05 | Hero image specified / generated | Agent brief + **human** pick | See `IMAGE-BRIEF.md` |
| 06 | Word doc created and saved | Agent | SharePoint Blog folder |
| 07 | Card → `Waiting Approval`, reviewers notified | Agent | Asana → Teams |
| 08 | Draft reviewed and marked up | **Human** — Matt / Bill | Word doc + Asana comments |
| 09 | Revisions implemented | Agent | Repo + SharePoint |
| 10 | Final approval | **Human** — Matt & Bill | Asana → `Approved Blogs` |
| 11 | Published | Agent | WordPress (Novamira) |
| 12 | Card → `Posted Blogs`, live URL recorded | Agent | Asana |

Stage 09 may loop back to 08 more than once before reaching 10.

Human gates: **03** (Thursday 1:1 triage), **08** (review, including the PPE check in §6) and
**10** (final approval). Stage 05 is automated as of 2026-09-10.

---

## 3. System IDs

### Asana — project `1216998438394279` (Blog Content Pipeline)

| Section | ID |
|---|---|
| Unapproved Ideas | `1216998438394303` |
| Approved Ideas | `1216997967900169` |
| Waiting Approval | `1216997967900170` |
| Approved Blogs | `1216997967900172` |
| Posted Blogs | `1216997967900173` |

### Teams — `Blog Ideas` channel

Read the full thread with `read_resource`, URI:

```
teams:///teams/da51070c-6c74-4d86-ab65-d67200f4cb83/channels/19:O6nGolAKJEPL830R4tiNfjUXqUBdhoZ9RMDuaCIGcgI1@thread.tacv2/messages
```

Returns every message chronologically, newest first — no keyword matching, no relevance
ranking. Walk newest → oldest and stop at the first message ID already captured as an Asana
task (the `Original message` permalink in existing Unapproved/Approved Ideas notes is the
watermark). Everything above the watermark is new.

### SharePoint — Blog folder

- `driveId`: `b!rFOk2NgZLUanLuEhSAQO6XVd1ws0aSJIhZeZ6Guiew2nCeXLAPUoQ41jyCucuNy_`
- parent folder item: `01W45A5ES5A7J7CNKQJBB2NGCR4RZJPRDS`

### WordPress

Published through the `novamira-chelectric-com` connector.

---

## 4. Known tool limits

**Asana cannot move a task between sections.** The connector exposes section placement only
at task creation; there is no move operation. Stages 07, 12 and the publish handoff therefore
cannot complete their card move by API today.

**This also breaks the Teams alert — the comment does NOT trigger it.** Earlier versions of
this playbook claimed a ready-for-review comment surfaces as a Teams notification. Observed
2026-09-11: the Friday run assigned Matt, added Bill as a follower and posted the comment at
13:49 UTC, and no Teams alert appeared. The alert only fired when a human dragged the card into
Waiting Approval at 14:39. Two things are working against it:

1. **The Asana→Teams integration is keyed to the section change,** which is precisely the one
   action the connector cannot perform.
2. **Everything the agent does in Asana is attributed to Matt Pocock,** because the connector
   authenticates as him. Every agent comment in the task history shows `created_by: Matt
   Pocock`. Asana does not notify you about your own comment or your own assignment, so the
   handoff is invisible to the very person it is addressed to.

Until §7 is configured, a completed draft sits silently until someone happens to look. Treat
the "please drag this card" line in the run's comment as the actual handoff mechanism, and know
that nobody is told it is there.

Until the custom-field workaround in §7 is in place: do the real work, comment on the card
saying exactly which section it needs to be dragged to, and say so plainly in the run
summary. Never pretend the move happened.

**No image-generation connector is installed.** See §6.

**LibreOffice is broken in this environment.** Do not rely on rendering to validate a
`.docx`. Validate by unzip integrity plus an XML parse of every part.

**Binary uploads to SharePoint are capped at roughly 18 KB in practice.** Verified against the
tool schema 2026-09-11: `sharepoint_upload_file` accepts only `content` (text) or
`contentBase64` (one unbroken base64 string in the tool call). There is no file-path argument
and no chunked upload — the schema says so explicitly. So every uploaded byte has to pass
through the model's own output, and two runs found the reliable ceiling to be about **25,000
base64 characters, roughly 18 KB of binary**. Past that, transcription introduces
single-character errors and the upload is correctly rejected.

Consequences, all of them real:

- A `.docx` must come in under ~18 KB **including** any embedded image. That leaves room for a
  preview of roughly 300–400 px, which is enough to judge composition and spot a PPE problem,
  and not enough for anything finer.
- **Uploading the full-resolution `hero.jpg` as a separate file does not work either** — same
  ceiling, same mechanism. The existing `Ultrasonic-Testing-Hero-Preview.jpg` in the Blog
  folder is 6 KB, which suggests whoever made it hit exactly this wall.
- The full-resolution original stays in git and goes to WordPress at publish time, where the
  Novamira connector handles it — that path does not go through this ceiling.

If reviewers need to see the hero at full quality before approval, the image has to reach them
by some route other than a SharePoint upload. See §6.

---

## 5. Failure handling

Applies to every stage.

**Check before you build.** Before starting work that depends on a write tool
(`mcp__Microsoft_365__sharepoint_upload_file`, the Novamira abilities, Asana writes), confirm
the tool is present — `ToolSearch` for it by exact name. Connectors are often mid-reconnect at
the start of a run, so search again before concluding one is gone. If `ListConnectors` shows
`connected: true` with `enabledInChat: false`, the connector is authenticated but toggled off
for the session — report it, because only a human can enable it.

**Never report a write you did not make.** Do not describe a file as saved, a post as
published, or a card as moved unless the tool returned success. Where a write returns a byte
count, confirm it matches the local file exactly — a truncated payload can pass validation and
silently write a corrupt file.

**Distinguish the two failure modes.**
- Tool absent, connector disconnected or not enabled → **transient**. Commit what is done,
  record state, stop that stage, let the next run retry.
- HTTP 403/407 from the egress proxy, or an explicit permission or policy denial → **do not
  retry and do not route around it.** Name the blocked host or permission and report it.

**Never half-complete a handoff.** Do not send a reviewer to a document that is not where the
notification says it is. If the draft could not be saved, leave the card in `Approved Ideas`,
do not assign reviewers, and record state. A review request with a dead link is worse than a
late one.

**Record state in two places.** Commit to `pipeline/STATE.md`, and comment on the Asana task.
Name: which stage failed, which tool was unavailable, what work *is* finished, and what the
next run should pick up — precisely enough that the next run resumes instead of redoing it.

**Each Routine must have this repository selected in its own settings.** Root cause of two
failed runs on 2026-09-10: a session fired by a Routine could *read* this repo but was not
authorized to *push* to it, so no ledger entry and no draft ever landed.

**The fix is the "Select a repository" field** in the Edit-routine dialog at
claude.ai/code/routines, directly beneath the Instructions box. Set it to
`mpocockch/ch-content` on all four Blog Routines. That gives each fired session a proper
checkout with push access, and it is the field the API cannot set — `create_trigger` exposes
no repository parameter, which is why every Routine created from this session started with it
empty.

Do not go looking for a "Claude Code Remote" connector to add instead; it is not offered in
the connector picker. The connector list for these Routines is Asana, Microsoft 365 and, for
Publish, novamira-chelectric-com. Repository access is a separate setting from connectors.

Verify after setting it: a run's ledger entry appearing as a new commit on the branch is the
proof. Until it is set, expect every run to reach the push step and stop there.

**If git is unavailable, DELIVER THE WORK ANYWAY — never discard a finished draft.** The
2026-09-10 test run wrote a full draft and generated a hero image, then threw both away
because it could not push, citing the commit-before-upload rule. That was the wrong call and
the rule was wrong to invite it. Corrected order of preference:

1. Commit and push, then upload. This is the normal path.
2. If the push fails: **still upload to SharePoint**, prefixing the filename
   `UNVERSIONED — `, and **still deliver the file with `SendUserFile`** so it survives the
   container. The work existing in one place beats existing in none.
3. Either way, if the push failed, do **not** move the card and do **not** assign reviewers.
   Record state on the Asana task naming the blocker.

The prohibition is on **half-completed handoffs** — telling a reviewer something is ready when
it is not — never on saving finished work. Discarding a draft to honor a storage rule is a bug.

**Commit AND PUSH — a local commit is worthless here.** The container is ephemeral and is
reclaimed when the run ends, so a commit that is never pushed dies with it. Every run that
writes anything to this repo must finish with:

```
git add -A && git commit -m "..." && git push origin HEAD
```

then verify the push landed (`git fetch` and compare `HEAD` to the remote ref). If the push
fails, say so loudly in the run summary — an unpushed ledger entry means the next run cannot
see what this one did, which defeats the entire design.

This bit us on 2026-09-10: the first verification run of `Blog: Idea Capture` completed
normally in 3m47s but left no commit on the branch, because the Routine prompts said "commit"
and never said "push". `SendUserFile` is a convenience for the human, never the backup.

**Report the block plainly.** End every run by naming what could not be done and the specific
human action that would unblock it.

---

## 6. Hero images — a human step, by design

**Hero images are generated by hand in Google AI Studio** (aistudio.google.com), by Matt.
That is a browser UI, not an MCP connector, so no Routine can drive it — and there is no
image-generation connector installed in this org either. The old Routine called a
`gemini-image-gen` connector that does not exist (`ListConnectors`, checked 2026-09-10), which
is why every hero-image step in the previous build failed or was silently skipped.

So stage 05 is **agent brief → human generates → agent packages**:

1. The draft run writes `drafts/<slug>/image-brief.md` — a prompt written to paste straight
   into the AI Studio prompt box, plus composition notes and alt text. See
   `pipeline/IMAGE-BRIEF.md`.
2. Matt generates the image in AI Studio and saves it as `drafts/<slug>/hero.png`
   (16:9, ≥1600px wide).
3. The packaging step embeds whatever `hero.png` is present. If none is present it proceeds
   with a placeholder and says so — **a missing image must never block review of the text.**
   The text can be reviewed and the image dropped in before publish.

Because the image arrives after the draft, the Friday run normally hands off text-only and the
image lands during the review loop. That is the expected path, not a failure.

### Automating it via the Gemini API — VERIFIED WORKING 2026-09-10

`pipeline/bin/generate-hero-image.py` calls the Gemini API directly. Verified 2026-09-10:

- **The API host is reachable from these containers.** A keyless request to
  `generativelanguage.googleapis.com/v1beta/models` returns Google's own
  `403 PERMISSION_DENIED — "Method doesn't allow unregistered callers"`, not a proxy error,
  and the egress proxy reports `selective: false` with no relay failures. Note that the
  *docs* domain `ai.google.dev` IS blocked by the proxy, which is unrelated and harmless.
- **The billing account is paid Tier 1** (`mattpocock@chelectric.com`, cap $250), so image
  models are in scope for this key. An earlier check against a different, free account
  (`mdpocock24@gmail.com`) was what made this look impossible.

The script takes a prompt file and an output path, supports both auth modes above, and
**exits 3 when neither is configured — which the caller must treat as "use the manual brief",
not as a failure.** It discovers the image model from the models endpoint rather than
hard-coding one, so a model rename or retirement degrades to the next choice. It never prints
the key: a canary value passed as `GEMINI_API_KEY` appears nowhere in its output.

Verified 2026-09-10: exit 3 with no auth, exit 4 in proxy mode with no credential yet (the
call reaches Google and returns its own `PERMISSION_DENIED`), and a clean `400 API key not
valid` for a bogus key. The success path is still untested — see below.

**Where the key goes — NOT in GitHub, and not in this repo.** It goes on the *cloud
environment* the Routine sessions run inside (`env_01Ez371HQbzkEd8jfxtaAf3x`). At
claude.ai/code, click the cloud icon showing the environment name in the row above the message
box — there is no settings page or direct URL for it — then hover the environment and click the
gear that appears. The dialog holds name, network access, environment variables and setup
script. Two ways to store the key there:

- **API credential (preferred; Pro/Max plans only).** In the same dialog, below **Environment
  variables**, choose **Add credential** — type Bearer, allowed website
  `generativelanguage.googleapis.com`, custom header `x-goog-api-key`. The agent proxy attaches
  it after the request leaves the VM, so **the key never reaches Claude, the session's
  environment, or any command it runs.** Then set `GEMINI_AUTH=proxy` as an environment
  variable so the script omits `?key=` and lets the proxy authenticate. Requires an org admin
  role; the section does not appear on Team or Enterprise plans.
- **Environment variable (simpler, less private).** Add `GEMINI_API_KEY=<key>` in the
  **Environment variables** box, `.env` format, one `KEY=value` per line. Note the tradeoff the
  docs state plainly: *"Anyone who uses the environment can read the values."*

Either way: **never commit a key to this repo, and never paste one into a chat transcript.**
Variables are copied once at session startup, so a change takes effect on the *next* run — a
session already running keeps what it started with. There are two environments both named
"Default"; the Routines use `env_01Ez371HQbzkEd8jfxtaAf3x`, so edit that one.

**Verified end to end on 2026-09-10.** `GEMINI_API_KEY` is set on both Default environments.
A real run in a fresh session produced a photorealistic 1376x768 hero image (760,159 bytes)
via `gemini-3-pro-image-preview`, exit 0, empty stderr. Evidence is committed at
`drafts/_imagegen-test/` (the image plus a full report). Two defects that run exposed are now
fixed or documented:

- The API returns **JPEG bytes even when asked for a `.png` path.** The script now corrects
  the extension from the magic bytes, so a JPEG lands as `hero.jpg`. **Downstream, look for
  `hero.*`, never specifically `hero.png`** — anything trusting the extension would otherwise
  read a mislabeled file, and WordPress media handling is exactly that kind of consumer.
- Aspect came out **1376x768 (1.792), not a strict 16:9** (1.7778). Close, but crop-sensitive
  layouts must not assume exactness.

**A human must still eyeball the PPE before a generated image ships.** In the verification
image the gear read as credible arc-flash equipment at a glance — hard hat, gold-tinted face
shield, head sock, arc-rated coat — but it was *not* what you would specify for energized
480 V switchboard work: a coat-and-shield combination rather than a full suit and hood, and
plain leather gloves with no rubber insulating gloves underneath. C&H's readers do this for a
living and can spot it. Incorrect PPE in the hero image of an electrical safety post is a
credibility problem, not a styling one. The model also does not fully honor "no text in
frame": expect small illegible label-like marks, which are acceptable only because they are
unreadable rather than visibly garbled.
2. Run the script once by hand and confirm it writes a valid image. The no-key and
   usage-error paths are tested; **the live API call is not** — the session that wrote it had
   no key. Until that one run passes, treat this as untested code.
3. Only then record the working model name below. The draft Routine checks this section every
   run and uses a named tool if present, so nothing else needs editing.

**Operational risk worth fixing first: auto-reload is OFF** with a $24.37 prepay balance.
Gemini credits are spent before the service runs, so when the balance hits zero image
generation starts failing — quietly, in an unattended Friday run. Turn on auto-reload, or
accept that the pipeline silently reverts to manual briefs. Credits also expire a year after
purchase ($25 added 2026-08-05). At two posts a month the spend is negligible; the balance
running dry unnoticed is the real hazard, not the cost.

Named image tool: **`pipeline/bin/generate-hero-image.py`** (model
`gemini-3-pro-image-preview`, key mode). Verified 2026-09-10. Falls back to the manual AI
Studio brief automatically if the key is ever removed or the balance runs dry.

---

## 7. Planned: replace section moves with a custom field

Asana's API *can* set custom fields even though it cannot move tasks between sections. The fix:

1. Add a `Stage` single-select custom field to project `1216998438394279` with options
   matching the five sections.
2. Add a native Asana Rule: *when `Stage` changes → move task to the matching section.*
3. Agents set `Stage` via `asana_update_task`; the Rule performs the move.

Sections stay exactly as they are for human visibility. This removes three "please drag this
card" chores from the pipeline. **Requires a human with Asana project-admin rights** — record
here when done, and update §4.

Status: **not yet configured — now the highest-value fix in this playbook.** It solves two
problems at once: the card move, and the Teams alert that depends on it (§4). A Rule-driven
move is performed by Asana itself rather than by the agent-as-Matt, so the existing Teams
integration fires normally.

If the Rule route is unavailable, the fallback is to notify out of band rather than through
Asana: `mcp__Microsoft_365__outlook_send_mail` is available to these Routines and can email
Matt and Bill directly with the SharePoint link. Less tidy, but it does not depend on Asana's
notification wiring or on who the connector authenticates as.

---

## 7b. Reviewer notification by email — the working handoff

Because the Teams alert cannot fire (§4), **email is the handoff mechanism** until §7 is
configured. Verified 2026-09-11: the Microsoft 365 connector holds `Mail.Send`, so
`mcp__Microsoft_365__outlook_send_mail` works from a Routine session.

**Recipients** (confirmed from their own mail signatures, not guessed):

- Matt Pocock — `mattpocock@chelectric.com`
- Bill Concannon — `billconcannon@chelectric.com`

`People.Read` is NOT granted, so `search_people` returns 403. Do not try to resolve names
through the directory at run time; use the addresses above.

**When to send.** Exactly at the two handoff moments, and only when the artifact the mail
points at actually exists:

| Stage | Send when | Subject |
|---|---|---|
| 07 draft handoff | the SharePoint upload returned success | `Blog draft ready for review: <title>` |
| 09 revision ready | the revised doc saved back successfully | `Blog draft revised, ready for another look: <title>` |

**Never send** on a quiet run, when the upload failed, or twice for the same event. An email
saying something is ready when it is not is worse than no email — the same rule that governs
the Asana comment (§5, half-completed handoffs).

**Link, do not attach.** Attachments go through the same model-output base64 ceiling as
SharePoint uploads (§4), so they are impractical and would be low quality anyway. Send links:
the SharePoint document, and the Asana task.

**Body should contain**, in plain prose, not a form dump: what the post is and its angle in a
sentence; the SharePoint link; the Asana task link; the reminder to check the hero image PPE
before it ships (§6); and the current manual step — that the card needs dragging from Approved
Ideas to Waiting Approval, since the connector cannot move it.

Keep it short. These are two busy people, and the mail is a pointer, not a report.

## 8. Routine registry

All Routines: fresh session per firing, environment `env_01Ez371HQbzkEd8jfxtaAf3x`,
notifications on. Cron is **UTC** — the times below are US Eastern and shift by an hour at
daylight-saving changeover; re-check each November and March.

| Routine | Trigger ID | Cron (UTC) | Eastern | Stages | Connectors needed |
|---|---|---|---|---|---|
| Blog: Idea Capture | `trig_01KcHdSfdZpQpgNDr8CFAGmj` | `30 11 * * *` | 07:30 daily | 02 (+ research Mondays) | Microsoft 365, Asana |
| Blog: Weekly Draft (Friday) | `trig_01TETYWmmJXn4iPJjcnd4jiu` | `0 12 * * 5` | 08:00 Friday | 04–07 | Asana, Microsoft 365 |
| Blog: Review Loop | `trig_017V1PhyYC3FgRK113ysB1Jz` | `30 12 * * *` | 08:30 daily | 09 (+ stall alert) | Asana, Microsoft 365 |
| Blog: Publish | `trig_01PwUZUGC9u71a36xbMcoGhj` | `30 13 * * *` | 09:30 daily | 11–12 | Asana, novamira, Microsoft 365 |

The one human step on the weekly clock is not a Routine: **Thursday-morning triage in Matt and
Bill's 1:1** (§9). It feeds the Friday draft run.

**All four are currently DISABLED.** See §10 for what has to happen before they are switched on.
They were deliberately left off rather than allowed to fire half-equipped, because a Routine
that runs without its connectors produces exactly the silent partial failures this rebuild
exists to eliminate.

Retired 2026-09-10, left disabled rather than deleted so their run history survives:
`RETIRED — Blog Pipeline: Daily Maintenance` (`trig_01Bo6Ueo1h1y1NsaFd6CPa9h`),
`RETIRED — Blog Pipeline: New Draft Cadence` (`trig_01LffXzfaEVnXvs1auYDmn4x`).

**Connectors cannot be attached to a Routine through the API in this organization** — the
`create_trigger` tool rejects the parameter, and a Routine created that way stores none. They
must be attached by a human in the claude.ai Routines UI. Verify with `list_triggers`: a
healthy Routine shows a populated `mcp_connections`, not `[]`.

### Research pass (Mondays, inside Idea Capture)

A light pass — a handful of candidates, not a flood — for timely topics, added to
`Unapproved Ideas` with `Source: Agent Research`. Monday placement is deliberate: candidates
are in the queue three days before the Thursday 1:1 triage (§9), so they are reviewed in the
same pass as anything the team posted to Teams, and drafted that Friday.

Check existing Unapproved/Approved Ideas first to avoid near-duplicates. **If
`Unapproved Ideas` already holds roughly ten or more untriaged topics and few have been
promoted recently, add nothing and say so** — the bottleneck is review capacity, not idea
supply, and padding the queue is not progress.

Industry landscape to draw on:

- **Standards and trade press:** NFPA / Corey Hannahs, Jim Phillips (Brainfiller), Mike Holt
  Enterprises, NETA, EC&M, Electrical Contractor Magazine — NEC, 70E, 70B, arc flash.
- **Healthcare and facility management:** ASHE, NEHES, AMFP Connecticut, IFMA Connecticut,
  BOMA, SMRP.
- **Connecticut manufacturing and aerospace:** ACM / Hartford Aerospace Alley, ManufactureCT,
  CBIA, CCAT, CONNSTEP.

### Stall alert (inside Review Loop)

If a card has sat in `Waiting Approval` more than 5 days with no reviewer comment, post one
Asana comment tagging Matt and Bill. One nudge per card per week — do not re-nudge daily.
This makes the human bottleneck visible instead of silent.

---

## 9. Weekly human triage

Not automated, and deliberately so: **Thursday morning, 15 minutes, in Matt and Bill's
standing 1:1** — they promote ideas `Unapproved Ideas` → `Approved Ideas` in one batch pass.

Thursday is chosen to sit right before Friday's draft run: a topic approved in the 1:1 is
drafted the next morning, rather than waiting out the week. The cost of that tightness is that
a cancelled or rescheduled 1:1 leaves Friday with only whatever was already approved — which
is survivable while the backlog holds several approved topics, and worth watching if it
doesn't.

Friday's draft run takes the *oldest* topic in `Approved Ideas`. If that section is empty the
run posts a note and stops. Promotion is the throttle that sets real publishing volume; the
2-posts-per-month target means roughly one promotion every other week, not one per idea.

---

## 10. Activation checklist

The rebuild is in place but **the pipeline is switched off** pending two things only a human
can do. Recorded 2026-09-10.

**1. ~~Grant the Claude GitHub App write access to `mpocockch/ch-content`.~~ DONE 2026-09-10.**
The app was installed but scoped to a repository list that predated this repo. Both write
paths had been failing with `403` (`git push`, and `403 Resource not accessible by
integration` on the API contents endpoint). Adding `ch-content` to the app's selected
repositories fixed it; the branch `claude/blog-automation-process-flbewl` is now pushed and
verified against the remote.

**2. Attach connectors to each of the four Routines** in the claude.ai Routines UI — per the
table in §8. This cannot be done from the API in this org: `create_trigger` rejects the
parameter, so all four currently store `mcp_connections: []` and their sessions would have no
Asana, Teams, SharePoint or WordPress tools at all.

**3. Enable the four Routines** once 2 is done. They are disabled today; see §8.

### Optional, and worth doing

- **Asana `Stage` custom field + Rule** (§7) — removes three "please drag this card" chores.
- **Install an image-generation connector** (§6) — restores stage 05 to automation. Record its
  exact tool name in §6 and the draft Routine picks it up with no prompt change.

### Verifying it works

Fire `Blog: Idea Capture` manually before trusting the schedule. A healthy run reads this
playbook, reports what it captured, and appends an entry to `pipeline/STATE.md`. Check
`list_triggers`: a real run shows `last_run.finished_at` minutes after `fired_at`. A
`finished_at` within milliseconds of `fired_at` means nothing ran — that was the old
session-bound failure mode.
