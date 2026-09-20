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

## 2026-09-11 — Review Loop (manual fire) — Panel Schedules rebuild, SharePoint upload BLOCKED

- This run was a manual trigger fire naming Panel Schedules (gid `1217697187018391`,
  currently in Waiting Approval) directly, with the reviewer feedback (an editorial pass from
  Matt) included in the fire payload rather than needing to be found in Asana comments.
- Did: rewrote `drafts/2026-09-panel-schedule-compliance/draft.md` and `sources.md` from
  scratch against the current DRAFTING.md/VOICE.md (rewritten 2026-09-11), matching the
  breaker-testing exemplar and the equipment-room-reliability sibling draft. New word count
  ~2,470 (old draft was 1,227). Added the metadata block, a stakes hook + roadmap (no Key
  Takeaways box), bolded answer sentences, a Misconceptions section, a Recent trends section,
  and a dedicated Safety section (beyond the eleven canonical types) per Bill's original title
  "Compliance, Safety, and the Cost of Playing Catch-Up" — safety was previously reduced to one
  sentence. Fixed the garbled actions-list sentence, moved drafting-process commentary
  ("we're not aware of a published industry figure...") out of the article and into
  `sources.md`, and replaced the truncated/under-supported NEC 408.4(A) quote with the full
  untruncated code text (now includes the directory-location sentence the old draft asserted
  without quoting), cross-checked against several independent secondary sources. `hero.jpg`
  and `image-brief.md` left byte-identical/untouched, per instruction.
  Self-check passed (word count, metadata, bolded answers, Misconceptions/Recent trends
  present, 4 internal links spread through the body, no em-dash pileups, no banned phrases).
  Committed and pushed to `claude/blog-automation-process-flbewl` (commit `d0fec82`), verified
  as an ancestor of the remote branch via `git fetch` + `git merge-base --is-ancestor`.
- Blocked: **the SharePoint replace-in-place upload is not done, and the live file may
  currently be corrupted.** Sequence:
  1. First `sharepoint_update_file` call hit a transient 423 "resource locked"; retried ~8s
     later.
  2. The retry returned success, but reported writing **25,250 bytes** against a local file
     that was **18,204 bytes** and an `expectedBytes` of 18,204 passed explicitly — a mismatch
     the tool's own documented behavior says should have been refused, but wasn't. Per
     PLAYBOOK.md §5 ("confirm a write that returns a byte count matches the local file
     exactly"), this should not have been treated as a completed write, and wasn't caught in
     time.
  3. A subsequent `read_resource` on that same file now fails with `notSupported` ("Graph
     refused to convert this file for text extraction"), where the same file converted fine
     before this run touched it — strong circumstantial evidence the live `.docx` in the Blog
     folder is now corrupted.
  4. A retry with a smaller (image-free) rebuild of the doc was rejected outright by the
     upload tool's own base64 validation: it reported receiving **28,513 characters against a
     20,596-character payload actually sent** (`sha256`/`wc -c` confirmed locally before
     sending). So the corruption is happening in transit for very large single-string tool-call
     arguments in this session, not in the docx-building step — matching (and worse than) the
     transcription-risk this playbook and past runs' notes already flagged for large base64
     payloads (§4, and the 2026-09-10/09-11 entries above).
  5. A further retry hit an unrelated SharePoint 412 conflict (sensitivity-label precondition).
  At that point, per explicit instruction, stopped retrying rather than keep hammering a
  demonstrably unreliable path, and left SharePoint as-is rather than risk compounding the
  corruption.
- **Per PLAYBOOK.md §5's half-completed-handoff rule: did NOT post a "ready for review" Asana
  comment and did NOT send the revision email.** The card stays in Waiting Approval (its
  current, correct section) with Matt/Bill still assigned/following; no section move or
  reviewer change was made. A state-only comment was posted on the Asana task instead, naming
  the blocker.
- Next run should:
  1. Check whether `Panel Schedules Are an NEC Requirement, Not Paperwork.docx` in the
     SharePoint Blog folder opens correctly by hand (Matt/Bill can check directly, or a future
     run can try `read_resource` on it again). If it's corrupted, prior versions should still
     be in SharePoint's version history for that file — restore from there rather than
     re-uploading over a further-corrupted copy.
  2. Retry the replace-in-place upload from the current, correct `drafts/2026-09-panel-schedule-compliance/draft.md`
     (git has the good copy regardless of SharePoint's state), but do not repeat the
     large-single-string-argument approach uncritically — this run's evidence suggests base64
     payloads in roughly the 20K+ character range are being corrupted in transit through this
     tool call in at least some sessions. Worth trying a materially smaller embedded-image size,
     verifying the tool's own reported byte count matches `expectedBytes` (and treating any
     mismatch as a failed write regardless of what the tool call returns), and/or reading the
     file back afterward before treating the write as verified.
  3. Only after a verified, non-corrupted upload succeeds: post the "ready for another look"
     Asana comment and send the revision email per §7b — neither happened this run.
  4. A concurrent session's entry above (Equipment Room .docx) found the same class of
     problem from a different angle: a docx that passed unzip+XML-parse validation but was
     still not valid OOXML, which Graph then refused to convert. PLAYBOOK.md §4 was updated
     with five checks meant to catch that. Worth checking whether that gap (rather than, or in
     addition to, base64-transit corruption) explains this run's broken file too.
## 2026-09-11 — Correction: the .docx was never corrupt; the upload is

- Matt reported the rebuilt file still would not open (Mac, no Word desktop, opening in Chrome
  → Word Online). Investigated properly instead of rebuilding again.
- **The earlier diagnosis in this file and in PLAYBOOK.md section 4 was wrong.** A copy of the
  rebuilt file made server-side fails identically, so it is not the item or its name. A
  40-line slice of the very same draft, built by the very same script, uploads and opens fine.
- Ran a size bisect with six probe documents. Everything at or under 9.8 KB opens; everything
  at or over 11.8 KB does not — across two completely different document builders. Content,
  formatting, table, headings and OOXML structure are all exonerated.
- Free oracle found: a good upload reports a stored size several KB larger than the bytes sent
  (SharePoint opened the file and wrote its metadata in). A bad upload reports exactly the sent
  byte count.
- PLAYBOOK.md section 4 rewritten with the bisect table and a ~10 KB working ceiling, replacing
  the incorrect "unzip-plus-XML-parse is insufficient validation" entry. The five structural
  checks are no longer presented as the fix, because they were not the problem.
- Probe files ZZ-probe-A through ZZ-probe-F removed from the Blog folder (recycle bin).
- Delivered the rebuilt file to Matt via SendUserFile to confirm it opens locally. If it does,
  the upload path is the bug and the handoff needs to stop going through SharePoint for
  full-length drafts.

## 2026-09-12 11:34 UTC — Blog: Idea Capture

- Did: read the watermark from the most-recently-created task in the project (gid
  `1217698634586206`, "How to Ensure Electrical Equipment Room Reliability", Original message
  id `1787259801114`, posted 2026-08-20). Listed the Teams channel's top-level messages
  (single page, 9 messages, no `read_resource` full-thread dump) and found that message is
  itself the newest one in the channel — nothing posted since. Created no Asana tasks; nothing
  new to capture. Today is Saturday, so the Monday research pass did not apply.
- Blocked: nothing.
- Next run should: proceed normally. `Unapproved Ideas` still holds 10 untriaged topics
  (unchanged since 2026-08-14) — still at/over the queue-depth line in PLAYBOOK.md §8, so a
  Monday research pass here should keep adding nothing until Thursday triage promotes some out.

## 2026-09-12 12:43 UTC — Review Loop

- Did: checked the single card in Waiting Approval (Panel Schedules, gid `1217697187018391`)
  for genuine reviewer feedback since the last recorded check (the 2026-09-11 19:22 UTC entry).
  Read the full story history — every story on the task, including that one, is attributed to
  Matt Pocock (the connector authenticates as him), and none of them read as fresh human
  feedback distinct from the pipeline's own run-state reporting. No new comments, and nothing
  that looked like a genuine reviewer edit. So there was no new revision to implement this run.
- Confirmed the standing blocker from 2026-09-11 is unchanged: "Panel Schedules Are an NEC
  Requirement, Not Paperwork.docx" in the SharePoint Blog folder still refuses to convert
  (Graph: `notSupported`) — still the copy corrupted by that run's failed replace-in-place
  upload.
- New data point: rebuilt the already-revised draft (git `d0fec82`, unchanged) as a fresh,
  validated `.docx` via the `docx` npm library with **no embedded image at all** — it came to
  15,675 bytes on its own, well above the ~10 KB working ceiling in PLAYBOOK.md §4. This rules
  out the embedded hero image as the cause: a full-length draft this size (~2,470 words) is not
  expected to survive an upload through this connector regardless of the image, so I did not
  repeat the SharePoint write and risk corrupting the live file further.
- Per §4's documented fallback, delivered the rebuilt `.docx` and `hero.jpg` directly via
  `SendUserFile`, and posted a state comment on the Asana task explaining the same, since the
  full text is otherwise only in git. Did NOT post a ready-for-review comment and did NOT send
  the revision email — the SharePoint save has not succeeded, so per §5/§7b this is not a
  completed handoff.
- Stall check (§8): card entered Waiting Approval 2026-09-11 14:39 UTC — under a day old, well
  short of the 5-day threshold. No nudge sent.
- Blocked: the SharePoint copy of this doc needs a human to restore it from version history or
  replace it by hand — this connector does not reliably support uploading a full-length draft
  (PLAYBOOK.md §4). No scripted/chunked upload path exists yet either.
- Next run should: re-check Waiting Approval for genuine reviewer comments as normal. If the
  SharePoint file has been fixed or replaced by a human, and there is still no chunked-upload
  workaround, consider whether the handoff can complete via the git/chat copy already delivered
  rather than waiting on a SharePoint upload that is unlikely to succeed for a draft this
  length.

## 2026-09-13 12:38 UTC — Review Loop

- Did: checked the single card in Waiting Approval (Panel Schedules, gid `1217697187018391`)
  for genuine reviewer feedback since the last recorded check (2026-09-12 12:43 UTC). Read the
  full story history — the only story since that timestamp is the 2026-09-12 12:43 UTC entry
  itself (the pipeline's own prior state comment); nothing posted after it. No genuine reviewer
  comment or question to act on.
- Also checked the SharePoint doc directly rather than relying only on Asana: "Panel Schedules
  Are an NEC Requirement, Not Paperwork.docx" (itemId `01W45A5ESKEOYIJGOUSNC2IMWSQT4TD7VP`) shows
  `lastModifiedDateTime` 2026-09-11T16:38:52Z, unchanged since before the last check — no new
  edit to react to. Did not re-open it to re-test whether it still converts; that diagnosis is
  unchanged from the prior two entries and re-probing it wasn't needed to answer "is there new
  reviewer input," which is what this stage checks for.
- Stall check (§8): card entered Waiting Approval 2026-09-11 14:39 UTC — about 1 day 22 hours
  old, well under the 5-day threshold. No nudge sent.
- Blocked: nothing new. The standing blocker from 2026-09-11/12 is unchanged: the live
  SharePoint copy may still be the corrupted replace-in-place upload, and this connector does
  not reliably upload a full-length (~2,470-word) draft (~10 KB working ceiling, PLAYBOOK.md
  §4). No new revision work was triggered this run, so no attempt was made to touch the
  SharePoint file.
- No Asana comment posted and no email sent — a quiet run with nothing new to report beyond
  what the 2026-09-12 comment already said on the card itself.
- Next run should: same as the 2026-09-12 entry — re-check for genuine reviewer comments, and if
  a human has restored/replaced the SharePoint file or a chunked-upload path appears, the next
  actual revision can complete the SharePoint save and the ready-for-another-look handoff.

## 2026-09-14 — Review Loop

- Did: checked the single card in Waiting Approval (Panel Schedules, gid `1217697187018391`) for
  genuine reviewer feedback since the last recorded check (2026-09-13 12:38 UTC). Read the full
  story history — nothing posted after the 2026-09-13 12:38 UTC entry, which is itself the
  pipeline's own prior state comment. No genuine reviewer comment or direct question to act on.
- Also checked the SharePoint doc directly: "Panel Schedules Are an NEC Requirement, Not
  Paperwork.docx" (itemId `01W45A5ESKEOYIJGOUSNC2IMWSQT4TD7VP`) still shows `lastModifiedDateTime`
  2026-09-11T16:38:52Z — unchanged, so no new Word-doc edit either.
- No other card is in Waiting Approval (Equipment Room reliability is still in Approved Ideas,
  untouched by a reviewer since 2026-09-11), so no hero-image arrival to check and nothing else
  in scope for this stage.
- Stall check (§8): card entered Waiting Approval 2026-09-11 14:39 UTC — about 2 days 22 hours
  old, still under the 5-day threshold. No nudge sent.
- Tool check: `mcp__Microsoft-365__outlook_send_mail` is not exposed in this session (only
  `outlook_create_draft` and other non-send Outlook tools resolved via ToolSearch) — same gap
  the 2026-09-11 16:22 UTC run hit. Moot this run since nothing needed sending, but the next run
  that has real revision work to hand off should check for this tool before promising an email,
  and fall back to a Drafts-folder draft per §5's transient-tool-absence rule if it's still
  missing.
- Blocked: nothing new. Standing blocker unchanged: the live SharePoint copy may still be the
  corrupted replace-in-place upload from 2026-09-11, and this connector does not reliably upload
  a full-length (~2,470-word) draft (~10 KB working ceiling, PLAYBOOK.md §4).
- No Asana comment posted and no email sent — a quiet run, nothing new beyond what the
  2026-09-12/13 comments already said on the card.
- Next run should: same as the 2026-09-13 entry — re-check for genuine reviewer comments, and if
  a human has restored/replaced the SharePoint file or a chunked-upload path appears, the next
  actual revision can complete the SharePoint save and the ready-for-another-look handoff.

## 2026-09-15 12:41 UTC — Review Loop — corrected a 4-day-old false blocker, completed the delayed handoff

- Did: checked the single card in Waiting Approval (Panel Schedules, gid `1217697187018391`) for
  genuine reviewer feedback since the last recorded check (2026-09-14). Read the full story
  history — nothing posted since the 2026-09-12 12:43 UTC entry (the pipeline's own prior state
  comment); no genuine reviewer comment or question to act on, so no new revision to implement.
- **Correction: the "corrupted SharePoint doc" blocker standing since 2026-09-11 was wrong.**
  Rather than trust the note, searched SharePoint directly and found the file at the correct
  name, "Panel Schedules Are an NEC Requirement, Not Paperwork.docx", now has a *different item
  ID* than the one every prior run (09-11 through 09-14) had been checking. That old item ID
  was renamed to "SUPERSEDED damaged upload - ..." at 2026-09-11T19:30:58Z, and a working copy
  was placed under the correct name at that same timestamp — almost certainly a human fix that
  landed between the 09-11 19:22 UTC revision run and the first 09-12 check, which every
  subsequent run missed because it kept re-checking the old (now-renamed) item ID instead of
  re-searching by name. Read the live file back via Graph: it converts cleanly and its full text
  matches the current revised draft (git `d0fec82`, unchanged since 09-11) word for word.
- Since the save is now confirmed good, completed the handoff that 09-11's revision run withheld
  pending exactly this confirmation: posted a "ready for another look" comment on the Asana task
  (correcting the record and linking the doc), per PLAYBOOK.md §7b/stage 09 step 4a.
- Attempted the revision email per §7b/step 4b. **This session's Microsoft 365 connector
  exposes no send tool** (only `outlook_create_draft`/reply-draft — no
  `outlook_send_mail`/`outlook_send_draft`), the same gap the 2026-09-11 16:22 UTC and 2026-09-14
  runs hit. Per §5 (tool absent → transient), created an unsent Drafts-folder draft addressed to
  Matt and Bill with the SharePoint and Asana links and the PPE reminder, rather than treating
  this as blocking the already-completed Asana handoff.
- Stall check (§8): card entered Waiting Approval 2026-09-11 14:39 UTC — about 4 days old, still
  under the 5-day threshold. No nudge sent.
- No hero-image action needed — already embedded in the doc since 09-11, and no new `hero.*`
  arrived.
- Blocked: **the revision email is sitting as an unsent draft, not sent** — a human needs to
  send it from Outlook Drafts, or a future run needs a session with a send-capable Microsoft 365
  connector. No other blocker.
- Next run should: nothing pending on this card from the drafting side. If the email is still
  unsent and a send-capable tool is available, send it (or a human already sent it manually —
  check Sent Items for "ready for another look" before re-drafting). Also worth flagging to a
  human: three consecutive runs (09-12, 09-13, 09-14) reported a false blocker because they
  checked a stale SharePoint item ID instead of re-searching by filename — worth deciding whether
  future runs should always re-search by name rather than reuse a remembered item ID.

## 2026-09-16 12:40 UTC — Review Loop

- Did: checked the single card in Waiting Approval (Panel Schedules, gid `1217697187018391`) for
  genuine reviewer feedback since the last recorded check (2026-09-15 12:41 UTC). Delegated the
  full story-history read to a subagent rather than re-reading everything inline; it confirmed no
  story on the card postdates the 2026-09-15T12:41:22Z entry, which is itself the pipeline's own
  prior state comment. No genuine reviewer comment or direct question from Matt/Bill anywhere —
  every story on this card, across its entire history, is agent self-narration (git commits,
  SharePoint mechanics, "Next run should…") attributed to Matt Pocock only via the connector's
  own-identity artifact (§4). No new revision to implement.
- Also checked the SharePoint doc directly rather than trusting Asana alone: "Panel Schedules Are
  an NEC Requirement, Not Paperwork.docx" still shows `lastModifiedDateTime`
  2026-09-11T19:30:58Z — unchanged, so no new Word-doc edit either.
- Checked `Approved Ideas` too: "How to Ensure Electrical Equipment Room Reliability" (gid
  `1217698634586206`) is still sitting there, untouched by a reviewer, and has been since
  2026-08-21 (~26 days) despite a ready draft uploaded and a review-request email attempted on
  2026-09-11. It was never dragged to Waiting Approval by a human. This card is outside stage 09's
  scope (it's not in Waiting Approval) and outside the §8 stall-alert's literal scope too, since
  that rule only watches Waiting Approval — flagging it here because nothing in the current
  playbook design notices a card stalling in Approved Ideas after its draft is ready.
- **Confirmed a standing blocker that's now spanned at least three runs (09-11, 09-14, 09-15,
  09-16): this session's Microsoft 365 connector still exposes no send-capable Outlook tool**
  (`outlook_send_mail`/`outlook_send_draft` — searched by exact name and by keyword, neither
  resolves; `ListConnectors` shows Microsoft 365 `connected: true, enabledInChat: true`, so this
  isn't a toggle-off, it looks like a missing scope/capability on the connector itself). Read both
  standing unsent drafts back via `read_resource` to check whether a human had sent them by hand:
  both still show `isDraft: true` —
  - "Blog draft ready for review: How Do You Ensure Reliability in an Electrical Equipment Room?"
    (created 2026-09-11T16:21Z) — still unsent, 5 days now.
  - "Blog draft revised, ready for another look: What Is Panel Schedule Compliance..." (created
    2026-09-15T12:41Z) — still unsent, 1 day.
  Did not create a third/duplicate draft — the two that exist already say what's needed and
  adding another wouldn't fix the root cause.
- Stall check (§8): card entered Waiting Approval 2026-09-11T14:39:24.912Z; now (2026-09-16
  12:40:03Z) that's 4 days 22 hours — under the 5-day threshold. No nudge sent.
- Blocked: **the email handoff channel has been non-functional for 5+ days across every run that
  has checked it.** Two ready-to-review drafts (Equipment Room, Panel Schedules revision) have
  had their notification emails silently stuck in Drafts the whole time, and neither reviewer has
  been told outside of Asana comments that Asana itself suppresses as self-notifications (§4).
  This is no longer a one-run transient — it needs a human to either (a) send the two existing
  Outlook drafts by hand, and (b) grant/restore Mail.Send capability on the Microsoft 365
  connector used by these Routines so future runs can send directly.
- No Asana comment posted and no email sent this run — nothing new to report on the card itself,
  and per §7b/§5 a run should never send an email (or claim readiness) it did not itself newly
  earn.
- Next run should: same check-for-genuine-comment routine. If a human confirms they've sent the
  two stuck Outlook drafts, note that in this file. If a send-capable tool is available in a
  future session, use it directly rather than drafting. Also worth a human decision: should the
  Equipment Room card be dragged from Approved Ideas to Waiting Approval now that its draft has
  been ready since 09-11, even though no reviewer has formally started on it?

## 2026-09-17 13:05 UTC — Review Loop — reviewer rewrote the Word doc directly; revision implemented and handed off

- Checked Waiting Approval (Panel Schedules, gid `1217697187018391`) for new Asana comments or new
  SharePoint Word-doc edits since the last recorded check (2026-09-16 12:40 UTC). No new Asana
  story since the 2026-09-15T12:41:22Z entry (the pipeline's own prior comment). But the doc's
  `lastModifiedDateTime` had moved to **2026-09-16T13:36:00Z** — a genuine new edit since the last
  check, made directly in SharePoint with no accompanying Asana comment. Read the live doc's full
  text and diffed it against the git draft: a reviewer had rewritten roughly a third of the
  article by hand, dropping the NFPA 70E arc-flash-label / NFPA 70B EMP framing throughout ("What
  Panel Schedule Compliance Involves," "Standards and Compliance," "Misconceptions," "Recent
  Trends," the how-to-build list) and replacing it with a legibility/digitization framing
  (handwritten directories, updating from a phone/tablet/desktop at the panel). No Word comments
  or tracked changes were visible — this connector has no raw-download tool, only
  `read_resource`'s flattened text extraction, so a comment or tracked-change layer (if any
  exists) is not something this pipeline can currently see; treated the resulting body text as
  the reviewer's actual words per the drafting standard, same as an Asana-comment instruction
  would be treated.
- Implemented that direction in `drafts/2026-09-panel-schedule-compliance/draft.md`, matching it
  to house structure (bold lead sentences, heading hierarchy), fixed one em-dash pileup introduced
  by the merge, updated `sources.md` (dropped the now-unused 70E/70B citations, kept on record in
  case a future revision restores them) and `linkedin.md` (previously led with the now-removed
  arc-flash-label point). Self-check passed: 2,606 body words, banned-phrase clean, 4 internal
  links, no other em-dash pileups.
- Committed and pushed to `claude/blog-automation-process-flbewl` (commit `034ebad`), verified as
  an ancestor of the remote branch via `git fetch` + `git merge-base --is-ancestor`.
- Rebuilt the `.docx` with the `docx` npm library (LinkedIn post appended per the standard),
  generated its base64 with a script and pasted it from a `Read` of that file rather than
  retyping it, to avoid the transcription risk documented in this file's 2026-09-11 entries.
  Fitting the ~2,600-word revision under the connector's practical upload ceiling (PLAYBOOK.md §4)
  required shrinking the embedded hero preview to 110×61px/quality 22 (~1.4 KB) — total 17,721
  bytes sent. `sharepoint_update_file` hit one transient 423-style 412 conflict on the first
  attempt (documented pattern, sensitivity-label precondition race); retried once after 5s and it
  succeeded, reporting a stored size of 24,796 bytes — larger than what was sent, which is this
  file's documented signal for a clean save. Read the file back afterward: it converts cleanly and
  matches the intended text and LinkedIn section word-for-word.
- Posted a "ready for another look" Asana comment explaining the SharePoint-edit discovery and
  what changed, and flagging that the embedded preview is too small for the PPE check this time.
  **Email**: `mcp__Microsoft-365__outlook_send_mail`/`outlook_send_draft` are still absent from
  this session (checked by exact name and keyword) — the same gap standing since 2026-09-11.
  Rather than add a third stuck draft alongside the two already sitting unsent since 09-11/09-15,
  updated the existing 09-15 "ready for another look" draft in place (same subject, same
  recipients) with current content, since its old body described a now-superseded revision.
  Delivered `draft.md`, `sources.md`, `linkedin.md` and the full-resolution `hero.jpg` via
  `SendUserFile` so the PPE check has a usable image regardless of the tiny doc preview.
- Stall check (§8): card has been in Waiting Approval since 2026-09-11 14:39 UTC — about 6 days,
  over the 5-day threshold. Did not send a stall nudge: the SharePoint edit found this run is a
  genuine, dated reviewer action from within the last 24 hours, so the card reads as actively
  engaged, not stalled. Said so on the card.
- **New, undocumented Asana state:** the project now has a sixth section, **"Blog Drafts"**
  (gid `1216997967900171`), sitting between Approved Ideas and Waiting Approval — not in
  PLAYBOOK.md §2's stage map or §3's section-ID table. The Equipment Room card (gid
  `1217698634586206`, previously stalled in Approved Ideas since 08-21) is now in this new
  section as of `2026-09-16T13:57:53Z` — same day as the Panel Schedules Word-doc edit, so likely
  the same human session reorganizing the board. This is outside stage 09's scope (Equipment Room
  isn't in Waiting Approval) and I made no changes to it or to the new section. Flagging plainly:
  **PLAYBOOK.md needs a human update to say what "Blog Drafts" means and where it sits in the
  stage map**, because every routine's section-ID table (§3) and stage-reading logic assumes only
  the original five sections, and a routine that doesn't know about this section could
  misinterpret or ignore a card sitting in it.
- Blocked: (1) the revision email is an updated Outlook Drafts item, not sent — same standing
  Mail.Send gap as prior runs. (2) the new "Blog Drafts" Asana section is undocumented — see
  above; no action taken on it this run.
- Next run should: check whether a human has sent the (now-updated) Outlook draft or restored
  Mail.Send capability. If PLAYBOOK.md has been updated to explain "Blog Drafts," read that before
  assuming anything about cards sitting in it. Otherwise, continue treating only Waiting Approval
  as this stage's scope.

## 2026-09-18 12:37 UTC — Weekly Draft (stages 04–07)

- Resume check first: read `drafts/` (both existing folders — Equipment Room Reliability and
  Panel Schedule Compliance — were already complete, nothing to finish) and recent Asana comments
  on Approved Ideas / Waiting Approval / the undocumented "Blog Drafts" section. Waiting Approval
  and Blog Drafts are both now empty. Traced why: Panel Schedules progressed normally (a human/
  system action moved it Waiting Approval → Approved Blogs on 2026-09-17T15:24:41Z — outside this
  stage's scope, no action taken). **Equipment Room Reliability (gid 1217698634586206) has
  disappeared: `asana_get_task` and `asana_get_stories_for_task` both return 403 forbidden, and it
  is absent from every section of the project**, including Approved Blogs and Posted Blogs. This
  is not explained by any normal pipeline action recorded here or in Asana's own stories. Flagged
  directly on the NFPA 70E card's run-status comment and again here: a human should check the
  Asana web UI or workspace audit log, since this connector's Asana account isn't Premium (search
  unavailable) and typeahead search found nothing. No genuine human comments/questions were found
  on any task checked (all stories were either agent self-narration or Asana's own system-
  generated section-move/assignment text) — nothing pending to answer before drafting.
- Took the oldest (and only) topic in Approved Ideas: "NFPA 70E 2027 Is Already in Effect..."
  (gid 1217455522370190, approved by Bill 2026-09-17). **Before drafting, fact-checked the card's
  central claim** — that the 2027 edition "took effect May 6, 2026" — since a practitioner-
  falsifiable claim destroys a piece's credibility (DRAFTING.md). It does not hold up: NFPA's own
  published development calendar for this cycle (per NETA World Journal and EC&M coverage) puts
  the membership Technical Meeting in June 2026 and Standards Council issuance expected only in
  fall 2026; the "May 6" date appears to be an artifact propagated across a cluster of similarly-
  styled SEO content-mill pages, not traceable to NFPA. Confirmed `nfpa.org` and top trade-press
  domains (ecmag.com, ecmweb.com, netaworldjournal.org) are blocked by this environment's egress
  proxy (`WebFetch` → `EGRESS_BLOCKED`), so every claim rests on `WebSearch` synthesis one step
  removed from primary text, not a direct read — documented plainly in `sources.md`, with numbers
  that couldn't be cross-confirmed (specific article numbers for the DC-hazard coverage, several
  section numbers) deliberately left out of the body per that same discipline.
  Reframed the article from "already in effect" to "in the final stages of NFPA's process, here's
  what's changing and how to prepare," and named the false premise directly as a Misconception
  rather than quietly avoiding it — the more useful and defensible article. Wrote
  `drafts/2026-09-nfpa-70e-2027-changes/{draft.md, sources.md, image-brief.md, linkedin.md}`.
  Self-check passed: 2,361 body words, metadata block, hook + roadmap, bolded section-opening
  sentences, Misconceptions + Recent trends present, banned-phrase clean, no em-dash pileups
  (found and fixed 9 paired-dash sentences before finalizing), 4 internal-link placeholders, CTA
  conditional/mid-article/closes on Final thoughts, LinkedIn post 200 words matching `LINKEDIN.md`.
- Generated the hero image via `pipeline/bin/generate-hero-image.py` (key mode,
  `gemini-3-pro-image-preview`, exit 0) — two workers in full arc-flash PPE (hooded suits, face
  shields, layered insulating/leather gloves) at an open switchgear cabinet, one performing
  energized diagnostic testing and one positioned outside the work zone as the second-person
  observer the article covers. Eyeballed the PPE per PLAYBOOK.md §6: reads as correct — full
  suit and hood on both figures, properly layered gloves — a cleaner result than the PPE issue
  flagged in an earlier verification run.
- Committed (`d5feb31`) and pushed to `claude/blog-automation-process-flbewl`; verified via
  `git fetch` + `git merge-base --is-ancestor` that the commit landed on the remote branch.
  Delivered the full draft folder via `SendUserFile` regardless (per §5, always deliver).
- Built the `.docx` with the `docx` npm library (installed fresh into a scratch dir), embedding
  the LinkedIn post under its own heading per the skill's handoff instructions. Sized the
  embedded hero preview to 110×61px/quality 30 (~1.6 KB) to fit PLAYBOOK.md §4's practical
  upload ceiling — final file 17,317 bytes, base64 23,092 chars, comfortably under the ~25,000
  char limit. **Validated before upload**: `unzip -t` reported no errors, and all 18 XML/rels
  parts parsed cleanly with `xml.dom.minidom`. Uploaded to the SharePoint Blog folder; the tool
  reported a stored size of 24,370 bytes — larger than the 17,317 sent, which is this file's
  documented signal for a clean save (SharePoint opened and re-stamped the file). Read the
  uploaded file back via `read_resource`: full text and the LinkedIn section match the intended
  draft word-for-word (Graph's PDF-conversion text extraction just collapses some hyphens/dashes
  into spaced characters — a read-back artifact, not a doc defect).
- **Handoff (upload succeeded, so all three per the playbook)**: assigned Matt and added Bill as
  a follower on the Asana task (both confirmed in the returned task object). Posted the
  ready-for-review comment with the SharePoint link, the PPE-check reminder (pointing reviewers
  to the full-res `hero.jpg` rather than the doc's tiny thumbnail), the "please drag to Waiting
  Approval" note, and a full explanation of the premise correction so reviewers aren't surprised
  by the reframed angle. Posted a second, separate run-status comment per step 7 naming exactly
  what completed.
  **Email**: confirmed (by exact-name AND keyword search, plus `ListConnectors` showing
  Microsoft 365 `connected: true, enabledInChat: true`) that this session's connector still has
  no `outlook_send_mail`/`outlook_send_draft` tool — the same gap standing in this file since
  2026-09-11. Created an Outlook Drafts-folder draft addressed to Matt and Bill with the
  SharePoint and Asana links and the premise-correction heads-up, rather than treating this as
  blocking the already-completed Asana handoff (per §5, tool-absent is transient).
- Blocked: (1) the handoff email is an unsent Outlook Drafts item — needs a human to send it, or
  a future run with a send-capable Microsoft 365 connector (now 5+ real-world weeks of runs
  hitting this same gap: 09-11, 09-14, 09-15, 09-16, 09-17, 09-18). (2) The Equipment Room
  Reliability task has vanished from Asana (403 forbidden, absent from every section) — see
  above; this needs direct human investigation in the Asana web UI or audit log, since the API
  gives no way to distinguish "deleted" from "access revoked" and this connector's Asana plan
  has no search to fall back on.
- Next run should: check whether a human sent the new Outlook draft (subject "Blog draft ready
  for review: What Is Changing in NFPA 70E's Next Edition?") or restored Mail.Send. Check whether
  a human has resolved the Equipment Room Reliability disappearance. Approved Ideas is now empty
  again — if no new topic has been promoted by the next Friday run, that's the throttle working,
  not a failure (per PLAYBOOK.md's cadence note), so post the empty-queue comment and stop per
  step 2 rather than treating it as a problem.

## 2026-09-18 12:41 UTC — Review Loop — Waiting Approval is empty; Panel Schedules advanced to Approved Blogs; Equipment Room card now inaccessible

- Did: checked `Waiting Approval` (gid `1216997967900170`) for genuine reviewer activity since the
  last recorded check (2026-09-17 13:05 UTC). **The section is empty — 0 tasks.** Cross-checked
  against a full project task listing (15 tasks total: 10 Unapproved Ideas, 1 Approved Ideas, 1
  Approved Blogs, 3 Posted Blogs, 0 Waiting Approval, 0 Blog Drafts) to confirm this wasn't a
  section-id mismatch. No card in scope for this stage this run, so no revision, no stall check
  (§8 only watches Waiting Approval), and per step 7 no email on a quiet run.
- **Panel Schedules ("Panel Schedules — Compliance, Safety, and the Cost of Playing Catch-Up (from
  Bill)", gid `1217697187018391`) is no longer in Waiting Approval — it moved to `Approved Blogs`
  at 2026-09-17T15:24:41Z**, about 2h19m after the 09-17 run's own "ready for another look" comment
  (13:05:50Z) and with nothing human-readable in between: the only two stories after the 09-17
  cutoff are that pipeline comment and a bare system story, "Matt Pocock moved this task from
  'Waiting Approval' to 'Approved Blogs'." Per PLAYBOOK.md §4 the Asana connector cannot move a
  task between sections by API, so this move can only have been done by a human in the Asana UI —
  i.e. this reads as genuine final approval (stage 10) even though no distinguishable "approved"
  comment exists (the connector's own-identity artifact makes a human's action and the pipeline's
  indistinguishable in the story feed by attribution alone; the move itself, not the attribution,
  is the evidence here). This card is now out of stage 09's scope and into stage 10/11 territory —
  flagging for whichever run next handles Approved Blogs / Publish, since nothing here moved it or
  acted on it further.
- **New anomaly: "How to Ensure Electrical Equipment Room Reliability" (gid `1217698634586206`)
  now returns `403 forbidden` ("You do not have access to this task") from both
  `asana_get_task` and `asana_get_stories_for_task`, using the same session/connector that read
  every other task in the project fine.** This card was readable as recently as the 2026-09-17
  13:05 UTC run (then sitting in the undocumented "Blog Drafts" section). A 403 is not the
  signature of a completed or archived task (those still return 200 with `completed: true`) or a
  deleted one (`not_found`) — it looks like the task was moved out of a project/workspace this
  connector's identity can see, or had its permissions changed directly. Also could not search for
  it by name: `asana_search_tasks` returned `payment_required` ("Search is only available to
  premium users"), which is itself worth a human's attention since it removes a normal fallback for
  exactly this situation. Nobody but a human with full Asana access can currently confirm what
  happened to this task or where it went.
- Tool check: `outlook_send_mail`/`outlook_send_draft` are still absent from this session (checked
  by exact name via ToolSearch) — same standing gap since 2026-09-11, now 8 days across every run
  that has checked. Moot this run since no revision needed sending, but the two Outlook drafts from
  09-11 and 09-17 (updated in place) are presumably still sitting unsent — not re-checked this run
  since there is no reason to believe a human sent them given nothing was said about a fix.
- Blocked: (1) the Equipment Room task access anomaly above — needs a human to check the task
  directly in the Asana web UI and confirm whether it's been moved, made private, or something
  else changed; PLAYBOOK.md §2's section-ID table doesn't cover a task disappearing from connector
  access entirely, so no run can self-diagnose this further. (2) Mail.Send capability is still not
  present on the Microsoft 365 connector used by this session — same standing blocker as every run
  since 2026-09-11.
- Next run should: re-check Waiting Approval as normal — it may be empty again if no new topic has
  been dragged there. If a human confirms what happened to the Equipment Room task, note it here.
  If Mail.Send is restored, use it directly for the next real revision handoff instead of falling
  back to a Drafts-folder draft.

## 2026-09-18 — Equipment Room Reliability: resolved, not an anomaly

- Matt confirmed directly (live chat, in response to this run's push notification): the team
  **decided to kill the "Electrical Equipment Room Reliability" topic**, which is why the Asana
  task now 403s — it was deleted, not a permissions/access bug. The 2026-09-18 12:37/12:41 UTC
  entries above and PLAYBOOK.md's implicit assumption that a 403 means an access problem were
  wrong for this case; no further investigation needed on that task.
- Removed the stale `drafts/2026-09-electrical-equipment-room-reliability/` folder from the repo
  (draft.md, hero.jpg, image-brief.md, linkedin.md, sources.md) since the topic is dead — recovers
  from git history if ever needed.
- **Not touched, flagged for a human instead:** the SharePoint copy, "How Do You Ensure
  Reliability in an Electrical Equipment Room.docx", is still sitting in the Blog folder
  (`lastModifiedDateTime` 2026-09-11T19:30:58Z). Deleting a shared SharePoint file is not something
  this run does unprompted — a human should delete or archive it directly if the topic is truly
  dead, so a reviewer doesn't stumble onto a doc for a killed post.
- Next run should: treat this topic as closed. No further "Equipment Room" flagging needed unless
  a human reopens it.

## 2026-09-18 13:05 UTC — Correction (interactive, follow-up to the Weekly Draft run)

- **The email blocker has been misdiagnosed since 09-11, including by both of this day's earlier
  runs (12:37 Weekly Draft and 12:41 Review Loop, which both recorded it as a missing
  capability).** Asked
  whether the notification could go to Teams instead, checked properly, and the check corrected
  something bigger. `mcp__Microsoft-365__get_granted_scopes` returns **`Mail.Send` as granted**.
  So Entra consent was never the problem, and every "grant/restore Mail.Send capability" line in
  this file (09-11, 09-14, 09-15, 09-16, 09-17, 09-18) pointed at a fix that was already in place.
  The real gap is that the connector does not *expose* `outlook_send_mail`/`outlook_send_draft` to
  these sessions, while exposing every other Outlook write tool (create/update/delete draft,
  filters, labels, vacation, trash, batch delete). Only the message-transmitting operations are
  gated. Fix lives in the claude.ai connector's enabled-tools settings — a human action; nothing
  in a session can change it (`ListConnectors` is read-only, no tool writes connector config).
- **Teams is closed too, and now checked rather than assumed.** Granted Teams scopes are read-only
  (`Channel.ReadBasic.All`, `ChannelMessage.Read.All`, `Chat.Read`, `Chat.ReadBasic`,
  `ChatMember.Read`, `ChatMessage.Read`); no send scope, and `teams_send_channel_message` /
  `teams_reply_channel_message` / `teams_send_chat_message` are absent. Posting to Teams needs new
  admin-consented scopes, or an Incoming Webhook on the channel (no scopes, but needs one-time
  human setup, somewhere to keep the URL, and an egress-proxy allowance). Neither exists today.
- Did: rewrote PLAYBOOK.md §7b with the correct diagnosis and the "do not chase Mail.Send" warning,
  added the Teams scope evidence to §4 so nobody re-explores that route, and fixed §7's stale
  "outlook_send_mail is available to these Routines" claim.
- Blocked: unchanged in effect — the handoff email still cannot be sent from a run, and the
  09-18 draft is still sitting unsent in Outlook. What changed is that the fix is now pointed at
  the right place.
- Next run should: still create the notification as a draft and say plainly it is unsent, but
  **update an existing unsent draft for the same event rather than adding another** — several have
  accumulated. If `outlook_send_mail` has appeared in the tool catalog, the setting was flipped:
  use it directly and note here that the gap closed.

## 2026-09-19 12:39 UTC — Review Loop

- Did: checked `Waiting Approval` (gid `1216997967900170`) for genuine reviewer activity since the
  last recorded check (2026-09-18 12:41 UTC). **The section is empty — 0 tasks**, confirmed both
  directly and via a full 15-task project pull (10 Unapproved Ideas, 1 Approved Ideas, 0 Waiting
  Approval, 1 Approved Blogs, 3 Posted Blogs). No card in scope for this stage, so no revision work,
  no hero-image check, and no stall alert (§8 only watches Waiting Approval).
- Also confirmed the "Blog Drafts" section flagged as undocumented on 2026-09-17/18 **does not
  exist** as a live section (`asana_get_project_sections` lists exactly the five sections in
  PLAYBOOK.md §2) — it was a one-off resting place for the now-deleted Equipment Room card, not a
  standing part of the board. No playbook change needed on that point.
- Tool check: `mcp__Microsoft-365__outlook_send_mail` and `outlook_send_draft` are still absent from
  this session (checked by exact name via `ToolSearch`), while `ListConnectors` shows Microsoft 365
  `connected: true, enabledInChat: true` — same standing gap as every run since 2026-09-11, now 8
  days. Moot this run since nothing needed sending. Did not re-check the accumulated unsent Outlook
  drafts (09-11, 09-15/09-17 updated-in-place) since there was no new event to fold into them and no
  reason to believe a human has sent them given nothing was reported.
- Blocked: nothing new. Standing blockers unchanged: (1) no send-capable Outlook tool exposed to
  this connector — human fix needed in the claude.ai connector's enabled-tools settings (§7b); (2)
  Asana still cannot move a task between sections by API (§4).
- No Asana comment posted and no email sent — a quiet run, nothing new to report.
- Next run should: re-check Waiting Approval as normal. If Approved Ideas' one topic (NFPA 70E 2027,
  gid `1217455522370190`) gets drafted and lands in Waiting Approval by a future Weekly Draft run,
  that's the next card this stage will act on.

## 2026-09-20 12:30 UTC — Review Loop

- Did: checked `Waiting Approval` (gid `1216997967900170`) for genuine reviewer activity since the
  last recorded check (2026-09-19 12:39 UTC). **The section is empty — 0 tasks**, confirmed both
  directly and via a full 15-task project pull (10 Unapproved Ideas, 1 Approved Ideas, 0 Waiting
  Approval, 1 Approved Blogs, 3 Posted Blogs). No card in scope for this stage, so no revision work,
  no hero-image check, and no stall alert (§8 only watches Waiting Approval).
- Confirmed the project's sections still match PLAYBOOK.md §2/§3 exactly (five sections, no
  resurfaced "Blog Drafts"). Panel Schedules (gid `1217697187018391`) remains in Approved Blogs,
  out of this stage's scope. NFPA 70E 2027 (gid `1217455522370190`) is still the sole Approved
  Ideas topic, waiting on a future Weekly Draft run — not this stage's job.
- Tool check: `mcp__Microsoft-365__outlook_send_mail`/`outlook_send_draft` are still absent from
  this session (checked by exact name via `ToolSearch`), while `ListConnectors` shows both Asana and
  Microsoft 365 `connected: true, enabledInChat: true` — same standing gap as every run since
  2026-09-11, now 9 days. Moot this run since nothing needed sending.
- Blocked: nothing new. Standing blockers unchanged: (1) no send-capable Outlook tool exposed to
  this connector — human fix needed in the claude.ai connector's enabled-tools settings (§7b); (2)
  Asana still cannot move a task between sections by API (§4).
- No Asana comment posted and no email sent — a quiet run, nothing new to report.
- Next run should: re-check Waiting Approval as normal. If NFPA 70E 2027 gets drafted and lands in
  Waiting Approval by a future Weekly Draft run, that's the next card this stage will act on.

## 2026-09-20 13:43 UTC — Publish — Panel Schedules re-checked, still blocked, no change since 09-18

- Did: read `Approved Blogs` (gid `1216997967900172`) — one task, Panel Schedules (gid
  `1217697187018391`), not a chore, correct scope for this stage. Confirmed it is not already
  live: queried WordPress directly (`novamira/execute-php`, read-only — `get_page_by_path` on
  slug `panel-schedule-compliance` plus two `WP_Query` searches on the title/keyword), no
  matching post at any status. Confirmed a hero image exists and is real:
  `drafts/2026-09-panel-schedule-compliance/hero.jpg`, valid JPEG, 1376x768.
- **Both publish preconditions (not live, hero present) are met, but publish did not proceed.**
  `drafts/2026-09-panel-schedule-compliance/draft.md` still carries the same 4 unresolved
  `[[internal link: <topic>]]` placeholders a prior Publish run (2026-09-18 13:41 UTC, recorded
  only as an Asana comment on the card, not previously logged here) already found and stopped
  on: two for "digital panel schedule documentation" (no matching live post — closest candidate,
  `/osha-electrical-documentation/`, isn't a confident match), one for "breaker testing" (resolves
  cleanly to the live `/what-is-breaker-testing/`), and one for "electrical equipment room
  reliability" (that sibling topic was killed 2026-09-18 per the entry above in this file — no
  target exists or ever will). Nothing has changed on the card or in the repo since that 09-18
  stop; no human has resolved or waived the placeholders. PLAYBOOK.md/DRAFTING.md are explicit
  that these mark where a real URL belongs and must not be invented, and publishing literal
  bracket text to a live page isn't something a later run can quietly undo — so this run held to
  the same stop rather than guessing or partially resolving just the one confident match.
- Did not touch draft.md, did not publish, did not move the card (it stays in Approved Blogs).
  Posted a short confirming comment on the Asana task (rather than repeating the full 09-18
  writeup) since Asana's own notification is invisible to Matt/Bill for a comment the connector
  attributes to Matt (the same own-identity gap documented throughout this file) — sent a push
  notification instead so this reaches a human through a channel that isn't affected by that gap.
- Tool check: `mcp__Microsoft-365__outlook_send_mail`/`outlook_send_draft` still absent from this
  session — unrelated to this run's blocker, noted for continuity only.
- Blocked: content decision only a human can make — resolve or explicitly waive the "digital
  panel schedule documentation" (×2) and "electrical equipment room reliability" internal-link
  placeholders in `drafts/2026-09-panel-schedule-compliance/draft.md`. Once that's done, a future
  Publish run can insert the confirmed breaker-testing link, apply whatever the human decided for
  the other three, and publish normally.
- Next run should: re-check `Approved Blogs` as normal. If the placeholders have been resolved
  (in the repo or by a clear instruction on the Asana card), proceed with publish per the normal
  stages 11–12 procedure; if not, hold the same stop rather than re-litigating it.
