---
title: "Panel Schedules Are an NEC Requirement, Not Paperwork"
slug: panel-schedule-compliance-nec-408-4
target_keyword: panel schedule compliance
asana_task: "1217697187018391"
status: drafting
---

## Key takeaways

- NEC 408.4(A) requires a legible, specific circuit directory on every panelboard,
  switchboard and switchgear — "spare" is fine for an unused breaker, "misc" or a tenant name
  that will change is not.
- That directory is a separate requirement from the arc-flash label under NFPA 70E 130.5(H).
  One identifies what a circuit feeds; the other tells a qualified person what PPE the
  equipment demands. Facilities often have one and assume it covers both.
- NFPA 70B became a mandatory standard in its 2023 edition. Panel documentation now sits
  inside a facility's required Electrical Maintenance Program record-keeping, not outside it.
- A stale directory is a code violation on its own, independent of whether the wiring behind
  it is safe. An inspector or insurer doesn't need to find a hazard to write it up.
- Updating a directory at the time of each circuit change is inexpensive. Reconstructing one
  years later — tracing every circuit in an energized panel from scratch — is not.

## What NEC 408.4(A) actually requires

Every circuit in a panelboard, switchboard or switchgear must be identified clearly enough
that someone can tell what it feeds without guessing. The code's own words, from the 2023
NEC:

> "Every circuit and circuit modification shall be legibly identified as to its clear,
> evident, and specific purpose or use. The identification shall include an approved degree
> of detail that allows each circuit to be distinguished from all others. Spare positions
> that contain unused overcurrent devices or switches shall be described accordingly...
> No circuit shall be described in a manner that depends on transient conditions of
> occupancy."

Three things fall out of that wording directly. First, "spare" is an acceptable, specific
label for an unused breaker — the code names it. Second, the directory has to live somewhere
findable: on the face of the panel, inside the door, or in an approved location right next to
it for a panelboard, and at each breaker or switch for switchboards and switchgear. Third, the
last sentence rules out exactly the kind of directory most facilities actually have: one
built around who currently occupies a space or which department a load happens to serve this
year. When that tenant moves out or the org chart changes, the directory is wrong — and it
was written in a way the code specifically prohibits.

## The circuit directory and the arc-flash label are not the same document

NFPA 70E 130.5(H) requires equipment likely to be examined, adjusted, serviced or maintained
while energized — switchboards, panelboards, industrial control panels, motor control
centers — to carry a field-applied label. That label has to show the nominal system voltage
and the arc-flash boundary, plus at least one of: incident energy and working distance,
minimum arc rating for clothing, or a PPE category. It exists to tell a qualified person what
to put on before they open the door.

The 408.4(A) circuit directory answers a different question: what does breaker 14 actually
feed. A facility can have a current, correctly formatted arc-flash label and a circuit
directory that hasn't been touched since a 2019 renovation. Both are required. Neither
substitutes for the other, and an auditor checking one won't assume the other is current.

The two also update on different clocks. NFPA 70E requires the risk assessment behind the
arc-flash label to be reviewed periodically, at intervals not exceeding 5 years, or sooner if
a change to the system could affect the numbers — new equipment, protective-device setting
changes, a utility service change. The circuit directory has no such fixed interval. Section
408.4(A) ties it to the event instead: "every circuit and circuit modification" gets
identified at the time of the modification. There's no 5-year grace period for a directory
that's been wrong since the day a circuit was added.

## Where NFPA 70B fits

NFPA 70B moved from a recommended practice to a mandatory standard with its 2023 edition.
That shift matters here because it requires an equipment owner to implement and document an
overall Electrical Maintenance Program (EMP) — and current, accurate panel documentation is
the baseline record that program is built on. A maintenance program that doesn't know what a
circuit feeds can't schedule inspection or de-energization work around it correctly. Treat
panel-schedule accuracy as part of the EMP's documentation obligation, not as a separate,
lower-priority housekeeping task.

## Why catching up costs more than staying current

None of this requires exotic tooling — a legible label maker and five minutes per circuit
change. The cost shows up on the other end, when nobody has done that for years and someone
has to reconstruct a directory for an entire facility at once.

Reconstructing a directory after the fact usually means tracing circuits with a toner and
receiver one at a time, checking with every affected department before a breaker gets
switched, and, for anything that can't be traced safely energized, arranging a shutdown
window. None of that scales the way updating one circuit at the time it changes does. The
practical framing is Bill Concannon's: it's easier to stay ready than to get ready. A
directory kept current breaker-by-breaker never becomes a facility-wide tracing project.

We're not aware of a published industry figure for the cost difference between incremental
labeling and a full facility retrace, and we won't invent one — if you have real numbers from
your own facility's experience, they'd make a more useful data point than an estimate.

## What to do about it

- Update the circuit directory at the time of any circuit change, not on the next
  inspection cycle. This is what 408.4(A) actually asks for.
- Confirm the arc-flash label under 70E 130.5(H) and the 408.4(A) circuit directory both
  exist and are both current — check for one and assume it covers the other, and you're
  likely missing the other.
- Fold panel documentation into your NFPA 70B Electrical Maintenance Program records rather
  than treating it as separate paperwork.
- If your directories have drifted for years, treat reconstruction as its own scoped project
  with a shutdown window, not something to squeeze into normal PM time.

[[internal link: NFPA 70B electrical maintenance program services]]
[[internal link: arc flash risk assessment and labeling]]

## FAQ

**Does every panel need a directory, even ones nobody normally opens?**
Yes. NEC 408.4(A) applies to every panelboard, switchboard and switchgear, not only the ones
serviced often.

**Is a printed schedule in the panel door enough, or do we need it recorded elsewhere too?**
The code only requires it be present at an approved location on or near the panel. But under
a documented NFPA 70B maintenance program, keeping a recorded copy alongside your other
maintenance records is what lets the program actually plan around it — the printed copy
alone doesn't feed into scheduling.

**How often does a circuit directory need to be updated?**
At the time of the circuit modification. 408.4(A) doesn't set a periodic review interval the
way 70E does for arc-flash labels — the obligation is continuous, triggered by each change.

## Call to action

If it's been more than a couple of years since your panel schedules were checked against
what's actually installed, have C&H verify them during your next scheduled maintenance visit
rather than waiting for an inspection to flag it.
