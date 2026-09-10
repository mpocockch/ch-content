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
