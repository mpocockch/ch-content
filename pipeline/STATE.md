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
- Next run should: nothing — all four Routines are DISABLED pending the activation checklist
  in PLAYBOOK.md section 10. GitHub write access for the Claude app is the hard blocker; the
  repo could not be pushed from the session that built it.
