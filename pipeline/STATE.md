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
