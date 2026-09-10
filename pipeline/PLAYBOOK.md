# Blog Content Pipeline — Playbook

The single source of truth for how a C&H Electric blog post gets from an idea in Teams to a
live page on chelectric.com. Every scheduled Routine starts by reading this file.

**Owners:** Matt Pocock, Bill Concannon
**Cadence target:** 2 posts / month. Drafting runs weekly (Friday); if no topic is approved,
the run stops cleanly — that is the throttle working, not a failure.

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

Human gates: **03, 08, 10** — plus the image pick at 05 until image generation is
re-automated (§6).

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

Until the custom-field workaround in §7 is in place: do the real work, comment on the card
saying exactly which section it needs to be dragged to, and say so plainly in the run
summary. Never pretend the move happened.

**No image-generation connector is installed.** See §6.

**LibreOffice is broken in this environment.** Do not rely on rendering to validate a
`.docx`. Validate by unzip integrity plus an XML parse of every part.

**Base64 payload ceiling on uploads.** File bytes are base64-encoded into the tool call, so a
full-resolution embedded image can exceed what one call can emit. Downscale the copy embedded
in the Word doc; keep the full-resolution original in the repo for the WordPress featured
image.

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

**Commit before you upload.** The container is ephemeral. Committing the draft and image to
`drafts/` is what makes the work survive; `SendUserFile` is a convenience for the human, not
the backup.

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

### Re-automating this later

Two routes, if the manual step becomes the bottleneck:

- **Gemini API key.** AI Studio issues API keys, and this environment has trusted network
  access, so a Routine could call the image endpoint directly over HTTPS. Store the key as an
  environment variable on `env_01Ez371HQbzkEd8jfxtaAf3x` (environment settings in the
  claude.ai UI — never commit a key to this repo) and record the variable name and endpoint
  here. Note the image models are generally paid-tier; verify the key's plan covers image
  generation before wiring it up.
- **An image-generation MCP connector,** if one is ever installed.

Either way: record the exact tool name or env var below. The draft Routine checks this section
for a named tool on every run and uses it if present, so no prompt change is needed.

Named image tool: _(none — manual via AI Studio, fallback to brief)_

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

Status: **not yet configured.**

---

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
`Unapproved Ideas` with `Source: Agent Research`. Monday placement is deliberate: it gives
reviewers the week to triage before Friday drafting.

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

Not automated, and deliberately so: **Monday, 15 minutes** — Matt and Bill promote ideas
`Unapproved Ideas` → `Approved Ideas` in one batch pass.

Friday's draft run takes the *oldest* topic in `Approved Ideas`. If that section is empty the
run posts a note and stops. Promotion is the throttle that sets real publishing volume; the
2-posts-per-month target means roughly one promotion every other week, not one per idea.

---

## 10. Activation checklist

The rebuild is in place but **the pipeline is switched off** pending three things only a human
can do. Recorded 2026-09-10.

**1. Grant the Claude GitHub App write access to `mpocockch/ch-content`.**
Without this the repo is unreachable and every Routine stops at its precondition, because the
playbook it needs to read is this file. Both write paths currently fail:

- `git push` → `403` — "Claude doesn't have GitHub access to mpocockch/ch-content for your
  organization"
- GitHub API contents endpoint → `403 Resource not accessible by integration`

Fix at https://github.com/apps/claude/installations/select_target (an org admin installs or
re-scopes the app to include this repo), or reconnect GitHub from claude.ai settings to
re-link an existing installation. Until then this repo exists only on the branch
`claude/blog-automation-process-flbewl` inside the session that built it.

**2. Attach connectors to each of the four Routines** in the claude.ai Routines UI — per the
table in §8. This cannot be done from the API in this org.

**3. Enable the four Routines** once 1 and 2 are done.

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
