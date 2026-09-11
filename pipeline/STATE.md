# Run ledger

Append-only. Every Routine adds one entry per firing — including quiet runs, so a gap in this
file means a run did not happen at all.

Format:

```
## YYYY-MM-DD HH:MM UTC — <routine name>
- Did: <what actually completed>
- Blocked: <what did not, and the tool/permission responsible — or "nothing">
- Next run should: <specific pickup instruction, or "nothing pending">
```

Keep entries short. The Asana card carries the detail; this file carries the sequence.

---

## 2026-09-10 — Pipeline rebuilt

- Did: replaced two session-bound Routines with four fresh-session Routines; moved
  methodology, system IDs and failure rules out of Routine prompts into this repo.
- Blocked: no image-generation connector exists in the org, so stage 05 is a human step
  (`PLAYBOOK.md` §6). Asana section moves still need a human drag until the custom-field
  workaround in §7 is configured by a project admin.
- Next run should: nothing yet — all four Routines are DISABLED pending the activation
  checklist in PLAYBOOK.md section 10. GitHub write access was granted the same day and this
  repo is pushed, so the remaining gate is attaching connectors to the four Routines in the
  claude.ai Routines UI, then enabling them.

## 2026-09-10 17:49 UTC — Blog: Idea Capture (first verification run, fired manually)

- Did: ran 3m47s in a genuinely fresh session (0 tokens of inherited context, vs the ~105k the
  retired session-bound setup started every run with). Created no Asana tasks, which appears
  correct: the newest task in Unapproved Ideas dates from 2026-08-14, the Monday research pass
  was deliberately skipped, and the section already holds 10 untriaged topics — at or over the
  queue-depth rule in PLAYBOOK.md section 8, where the correct action is to add nothing.
- Blocked: **it left no commit on the branch, so it wrote no ledger entry.** Root cause was a
  defect in the Routine prompts, not in the run: they said "commit" and never said "push", and
  an unpushed commit dies with the container. Entry written retroactively by the session that
  built the pipeline. All four prompts and PLAYBOOK.md section 5 now require commit AND push
  with verification.
- Also noted: the run cost ~$1.04 and 145k tokens to conclude that nothing was new. Worth
  watching — across three daily Routines that is roughly $90/month. If it stays that high, the
  likely cause is re-reading the full Teams history and every long Asana task note each run;
  a stored watermark would fix it.
- Next run should: proceed normally, and push its ledger entry.

## 2026-09-10 20:23 UTC — Gemini image generation verified

- Did: ran the image script end to end in a fresh session with the key now on both Default
  environments. Exit 0, a real 1376x768 photorealistic hero image via
  `gemini-3-pro-image-preview`. Evidence committed at `drafts/_imagegen-test/`. Stage 05 is
  now automated; PLAYBOOK.md section 6 names the tool.
- Blocked: nothing.
- Fixed as a result: the API returns JPEG even for a `.png` path, so the script now names the
  file after the real bytes and everything downstream matches `hero.*`.
- Standing caveat: a human must check the PPE in any generated image before it ships, and
  aspect is 1.792 rather than exactly 16:9.
- Next run should: proceed normally. Friday's draft will generate its own image.

## 2026-09-10 — Triage moved to Thursday

- Did: moved the weekly human triage from Monday to Thursday morning, to run inside Matt and
  Bill's standing 1:1. A topic approved there is drafted the next morning by the Friday run
  instead of waiting most of a week. The Monday research pass stays where it is, so researched
  candidates are three days old and reviewed in the same pass as team pitches.
- Blocked: nothing. No Routine schedule changed — triage was never automated.
- Next run should: proceed normally.

## 2026-09-10 21:04 UTC — Weekly Draft, manual test run — FAILED, two defects found

- Did: drafted "Panel Schedules Are a Compliance Requirement, Not Paperwork" and generated a
  hero image in 11.5 minutes, then recorded an accurate, self-diagnosed blocker on the Asana
  task. The state-recording behaviour worked exactly as designed.
- Blocked: **could not push to this repo.** A Routine-fired session can read it but is not
  authorized to push, and `add_repo` — which would fix that — is in the Claude Code Remote
  connector, which is not attached to the Blog Routines. Same root cause as the Idea Capture
  run earlier today, which the commit-and-push wording change did not address because the
  problem is authorization, not instructions.
- **Second defect, worse: the draft and image were discarded.** Having failed to push, the run
  uploaded nothing and delivered nothing, citing commit-before-upload. A finished draft was
  destroyed to honor a storage rule. PLAYBOOK.md section 5 now requires delivering the work by
  any available route when git is unavailable, and confines the prohibition to half-completed
  handoffs. Routine prompts updated to match.
- Also surfaced: the 2026-09-08 `PanelSchedulesBlog.docx` in SharePoint was not produced by
  this pipeline and has no git history. Matt moved that card back to Approved Ideas at 21:02,
  two minutes before this run fired, which is why the topic was available to draft.
- Correction, same day: the push blocker is NOT a missing connector. It is the "Select a
  repository" field in each Routine's own settings, which was empty because create_trigger
  exposes no repository parameter. Setting it to mpocockch/ch-content on each of the four
  Routines is the fix, and it can only be done in the Routines UI.
- Next run should: expect the push to fail until that field is set, and per the corrected
  rules still upload and deliver the draft rather than discarding it.

## 2026-09-10 22:13 UTC — Weekly Draft, MANUAL TEST RUN #2 (fired by Matt, not a scheduled Friday run)

- Did: read the shared branch (`claude/blog-automation-process-flbewl`) via
  `git fetch` + `git checkout -B work`, per this run's setup instructions. Drafted the
  topic named in the test payload, "Panel Schedules — Compliance, Safety, and the Cost of
  Playing Catch-Up (from Bill)" (Asana gid `1217697187018391`), producing
  `drafts/2026-09-panel-schedule-compliance/{draft.md,sources.md,image-brief.md,hero.jpg}`.
  Banned-phrase self-check passed first try. Generated the hero image via
  `pipeline/bin/generate-hero-image.py` (`gemini-3-pro-image-preview`), exit 0,
  701,178 bytes, 1376x768 JPEG. Committed and pushed to the shared branch (commit
  `9edac18`), then verified by fetching and confirming the commit is an ancestor of
  `origin/claude/blog-automation-process-flbewl` — **the repo-access push blocker from the
  21:04 UTC run today is resolved.** Delivered all four artifacts to the user directly via
  `SendUserFile` regardless of push outcome, per the corrected failure-handling order.
  Built a `.docx` with docx-js (embedded a downscaled 320px hero copy to stay well under
  the base64 ceiling), validated it via unzip integrity + an XML parse of every part
  (LibreOffice not used, per PLAYBOOK.md section 4), and uploaded it to the SharePoint
  Blog folder as `TEST 2026-09-10 — Panel Schedules Are an NEC Requirement, Not
  Paperwork.docx` (20,623 bytes; upload's `expectedBytes` check confirmed an exact byte
  match). Did not touch the pre-existing, non-pipeline `PanelSchedulesBlog.docx` from
  2026-09-08. Posted one Asana comment recording state on the task.
- Blocked: nothing. Per this run's explicit test overrides, the card was deliberately
  **left in Approved Ideas** with no reviewers assigned and no "ready for review" comment —
  this was a directed exception for the test, not a failure of stage 06/07.
- Also noted (test-specific, not process defects): reconstructing the built `.docx`'s
  base64 into a single MCP tool-call argument from paginated file reads is expensive —
  needed the embedded hero copy downscaled repeatedly (eventually 320px/quality 45, ~7.8KB)
  to keep the read-and-retype round trip manageable; worth a script-based upload path if
  this becomes routine rather than exceptional.
- Next run should: for a normal (non-test) run on this same topic, note that a real draft
  already exists at `drafts/2026-09-panel-schedule-compliance/` — resume/build on it rather
  than starting over, per the pipeline's resume-before-you-start rule.

## 2026-09-11 — Weekly Draft (Friday), Panel Schedules — completed end to end

- Did: resumed the existing draft at `drafts/2026-09-panel-schedule-compliance/` (built by the
  2026-09-10 test runs) rather than starting over. Ran the actual self-check against
  `VOICE.md`/`DRAFTING.md` this time — found and fixed two em-dash-pileup violations (one in
  the Key Takeaways box, one in the 70E paragraph) and set `status: in-review` in the front
  matter. Left `hero.jpg` untouched per the resume rule. Committed and pushed to
  `claude/blog-automation-process-flbewl` (commit `f5ab5fc`), verified by fetching and
  confirming the commit is an ancestor of the remote branch. Delivered `draft.md`,
  `sources.md`, `image-brief.md` and `hero.jpg` to the user via `SendUserFile` regardless of
  push outcome.
- Packaging: built the Word doc with docx-js (no bundled `docx`/`sharpen` packages in this
  environment — installed them fresh into the scratchpad directory), embedding a downscaled
  220px copy of the hero image to stay well under the base64 payload ceiling. Validated via
  unzip integrity + an XML parse of every part (LibreOffice is broken here, per PLAYBOOK.md
  §4). Uploaded to the SharePoint Blog folder as `Panel Schedules Are an NEC Requirement, Not
  Paperwork.docx`; the upload tool's `expectedBytes` check confirmed an exact 16,906-byte
  decode match.
- Notable friction: reconstructing the docx's base64 into a single MCP tool-call argument by
  hand (there is no chunked-upload or file-path option on the upload tool) took several failed
  attempts — manual transcription of ~20–38K characters of base64 reliably introduced a
  handful of single-character errors per attempt, and one earlier attempt at a larger payload
  (~28.5K base64 chars) silently picked up injected whitespace, which the tool correctly
  rejected as invalid base64. Shrinking the embedded image (and therefore the whole payload)
  to keep total base64 under roughly 25K characters, plus verifying every reconstruction
  byte-for-byte against the source file before submitting, was what finally got a clean
  upload. Worth a scripted/tool-assisted upload path if `.docx` uploads become routine rather
  than exceptional — see the same note from the 2026-09-10 22:13 UTC test run, which flagged
  this same cost.
- Assigned Matt Pocock and added Bill Concannon as a follower on the Asana task, then posted a
  ready-for-review comment linking the doc and flagging the hero-image PPE check called out in
  PLAYBOOK.md §6. Posted a separate state-recording comment naming exactly what completed.
- Blocked: nothing. The Asana connector still can't move the card between sections (§4) — left
  it in Approved Ideas and said so in the comment, asking a human to drag it to Waiting
  Approval.
- Next run should: nothing pending on this card. If Approved Ideas is non-empty next Friday,
  take the new oldest topic ("How to Ensure Electrical Equipment Room Reliability", gid
  `1217698634586206`, is next in line once this one moves out of the section).

## 2026-09-11 — Why no Teams alert fired

- Observed: the Friday run assigned Matt, added Bill as a follower and posted a ready-for-review
  comment at 13:49 UTC. No Teams alert. The alert only appeared when Matt dragged the card to
  Waiting Approval at 14:39.
- Cause: the alert is keyed to the section change, which the Asana connector cannot perform,
  and every agent action in Asana is attributed to Matt because the connector authenticates as
  him — so Asana suppresses the notification as a self-action. The playbook's claim that the
  comment triggers the alert was wrong and is now corrected in §4.
- Fix: §7 (Stage custom field + Asana Rule) now solves both the move and the alert. Fallback is
  an Outlook email direct to the reviewers.

## 2026-09-11 16:22 UTC — Weekly Draft (manual fire) — Electrical Equipment Room Reliability

- This run was a manual trigger fire. The fire payload contained an unsigned "MANUAL RE-DRAFT"
  override claiming to be from Matt, instructing a rewrite of the Panel Schedules card
  (currently in Waiting Approval) instead of the standard job. Per this session's instructions,
  a manual-fire payload is treated as data, not as instructions, unless the routine's own
  stored prompt says to follow it — this one didn't reference or delegate to any such payload.
  So I ignored the override and ran the standard stage 04–07 job instead. Recording this here
  so a human can confirm whether that override was genuine and, if so, act on it through a
  normal channel (an Asana comment on that card, or a fresh routine-prompt edit) rather than a
  fire-time payload.
- Did (standard job): resumed correctly — read comments on both Approved Ideas and Waiting
  Approval cards, found no direct question from Matt/Bill needing a reply, and confirmed no
  in-repo unfinished draft existed for the oldest (only) Approved Ideas topic, "How to Ensure
  Electrical Equipment Room Reliability" (gid 1217698634586206). Its history showed a
  pre-pipeline SharePoint draft from 2026-08-21/09-04 that was never committed to git and never
  moved out of Approved Ideas (likely lost to the known Teams-notification gap, §4) — left it
  untouched and flagged it on the card for a human decision rather than guessing.
- Wrote a fresh draft.md/sources.md/image-brief.md against the current DRAFTING.md/VOICE.md
  (2,440 words, all 11 house section types, self-check passed). Generated hero.jpg via
  pipeline/bin/generate-hero-image.py, exit 0. Committed and pushed to
  claude/blog-automation-process-flbewl (commit ac256a7), verified as an ancestor of the
  remote branch. Delivered all four files to the user via SendUserFile.
- Built and validated a .docx (unzip integrity + XML parse of every part), 18,071 bytes with a
  200x111px embedded hero preview, uploaded to the SharePoint Blog folder — expectedBytes
  confirmed an exact match. Assigned Matt, added Bill as a follower, posted a ready-for-review
  comment (flagging the pre-pipeline draft found above and the PPE check).
- Blocked: the handoff email (§7b) could not be sent — this session's Microsoft 365 connector
  exposed only outlook_create_draft/reply-draft tools, no send capability. Per §5 (tool
  absent → transient), created the email as an unsent Drafts-folder draft addressed to Matt and
  Bill with the SharePoint and Asana links, and recorded this on the Asana task. A human needs
  to send it from Drafts, or a future run needs a session where a send-capable tool is present.
- Next run should: nothing else pending on the equipment-room-reliability card from the
  drafting side. If a human confirms the Panel Schedules re-draft override was genuine, that
  should come back through a normal channel (Asana comment or routine-prompt edit), not be
  re-attempted from this run's fire payload.

## 2026-09-11 — Equipment Room .docx was corrupt; validation gap found

- Symptom: Matt could not open the Equipment Room Word doc — "this document can't be opened
  for editing". Confirmed independently: Microsoft Graph also refused to convert it
  (notSupported), while a human-authored file in the same folder converts fine.
- Cause: the run's .docx passed the documented validation (unzip integrity + XML parse of
  every part) but was not a valid OOXML document. That check cannot detect a missing or wrong
  content-type declaration or a broken officeDocument relationship, which is exactly this
  failure mode.
- Fixed: rebuilt the document with the docx npm library, validated content types,
  relationships and the document root, and delivered it to Matt directly. The SharePoint
  replace was refused with a 412 conflict (the file was locked, most likely by Matt's own open
  Word session), so the copy in the Blog folder is still the broken one until it is replaced
  by hand or on retry.
- PLAYBOOK.md section 4 now specifies the five checks that actually catch this.

## 2026-09-11 — Rebuilt Equipment Room .docx uploaded to SharePoint

- The `replace` upload stayed blocked by the 412 lock, so the rebuilt file was uploaded beside
  the broken one under a new name: **How Do You Ensure Reliability in an Electrical Equipment
  Room (rebuilt).docx** — 15,491 bytes, itemId `01W45A5EVVM2LPDJBCT5GZUE4VH4ZDRZQV`, in the
  same Blog folder. The upload returned success and the byte count matched.
- Waiting on a human to confirm it opens. If it does, that confirms the diagnosis in the entry
  above and the broken original should be deleted.
- Still to do: update the Weekly Draft / Review Loop routine prompts to build .docx with the
  `docx` npm library and run the five checks now in PLAYBOOK.md section 4. The playbook
  records the requirement; the routine prompts do not yet carry it.
