# Six authorities, six questions

Use existing project equivalents. These are semantic responsibilities, not a command to
create six empty documents for every task. When adopting the full workflow, establish
each needed register with real content and record its actual path in the agreement.

| Register | Answers | Change rule |
|---|---|---|
| Design/spec/PoC history | Why is this decision correct? | Timestamp files; retain discussion, conclusion, open questions, experiments, findings, pivots, blockers. After adoption append dated corrections rather than erasing history. |
| Limitations/deferrals | What is constrained, wrong, or postponed? | Update rows in place when resolved or narrowed. Distinguish accepted system limits from actionable deferred work. |
| Changelog | What changed in this PR? | Add one `changelog/<type>-<name>.md` with What and Verified plus an index row. Preserve published history. |
| Current system | How does it work now? | Update in the behavioral PR. Distinguish active, test-only, built-but-unwired, partial, and stubbed states. |
| Responsibilities | Who owns it, and what must it not do? | Update when ownership moves or a component is added, split, combined, removed, or promoted to runtime. |
| Delivery roadmap | What must be proven next? | Update gate order, scope, blockers, and status. Completion requires executable exit evidence through the real composition. |

Use `YYYY-MM-DD-HHMM-<subject>.md` for new design documents and record the timezone.
Follow the repository's timestamp convention. Changelog index rows normally contain
date, type (`feat`, `fix`, `docs`, `chore`, `refactor`), description, and entry link.

Cross-reference authorities. The system document explains constraints needed to understand
its mechanisms; the limitations register holds the defect list. The roadmap links findings
and exit criteria instead of repeating them. A passing isolated test or merged PR does not
by itself prove product readiness.

For retained review documents, record exact head/base commits and scope. Findings have
stable IDs and consequence-based priorities. Preserve findings with Open, Done, Ignored,
or Parked dispositions and evidence/rationale. Parked requires a reason deferral is safe,
a follow-up condition, and an owner/milestone where known. It is not automatic approval.
Keep raw transcripts local unless the repository explicitly requires publication.
