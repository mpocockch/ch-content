# ch-content

Durable state for the **C&H Electric Blog Content Pipeline**.

This repository is the pipeline's memory. Scheduled Routines run in *fresh, disposable
sessions* — nothing is remembered between runs except what is committed here and what is
recorded on the Asana cards. If a fact matters to the next run, it belongs in a file.

| Path | What it holds |
|---|---|
| `pipeline/PLAYBOOK.md` | Stage map, every system ID, the routine registry, failure rules |
| `pipeline/DRAFTING.md` | SEO drafting methodology |
| `pipeline/VOICE.md` | Tone, banned phrases, CTA rules |
| `pipeline/IMAGE-BRIEF.md` | How hero images are specified and sourced |
| `pipeline/STATE.md` | Append-only run ledger and handoff notes |
| `drafts/` | One folder per post: draft, sources, image brief, hero image |
| `.claude/skills/blog-draft/` | The drafting skill loaded automatically in this repo |

## Why it is built this way

The pipeline previously ran two Routines bound to a single long-lived chat session. That
session accumulated context until it wedged, and because the methodology lived only in the
conversation, every failure lost knowledge. Read `pipeline/PLAYBOOK.md` § Design rules
before changing how the Routines are wired.

Owners: Matt Pocock, Bill Concannon.
