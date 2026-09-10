# ch-content — orientation

This repo is the durable state for the **C&H Electric Blog Content Pipeline**. It is read by
scheduled Routines running in fresh, disposable sessions.

**Read `pipeline/PLAYBOOK.md` first.** It holds the stage map, every system ID (Asana
sections, the Teams channel URI, the SharePoint drive), the routine registry, known tool
limits, and the failure-handling rules. Do not re-derive any of that.

For drafting work, also read `pipeline/DRAFTING.md` and `pipeline/VOICE.md` — or invoke the
`blog-draft` skill, which loads both.

## Non-negotiables

- **Never bind a pipeline Routine to a persistent session.** `PLAYBOOK.md` §1 explains what
  happened last time.
- **Asana is the state machine.** Read a card's stage from its section; never assume it.
- **Commit AND push before you upload.** Git is the durable store; SharePoint and Word are
  the review surface. The container is reclaimed at the end of a run, so an unpushed commit is
  lost work — always `git push origin HEAD` and verify it landed.
- **Never report a write that did not return success** — not a saved file, not a published
  post, not a moved card.
- **Append to `pipeline/STATE.md` every run,** including quiet ones.

## Conventions

- Prose files are Markdown, wrapped at ~90 characters.
- Drafts live in `drafts/<YYYY-MM>-<slug>/` — see `drafts/README.md`.
- There is no build and no test suite; this repo holds documents and content, not code.
