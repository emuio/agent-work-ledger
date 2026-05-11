# Claude Code Agent Work Ledger Example

For complex tasks, use Agent Work Ledger as the visible work record.

## Working Agreement

1. Create or update a task event when work begins.
2. Keep one concrete next action.
3. Move blocked work to `WAITING`.
4. Move human decisions to `REVIEW`.
5. Attach evidence for files, commits, logs, reports, and links.
6. Mark work `DONE` only after the outcome is met and evidence exists.

## Human Checkpoints

Pause and request approval before:

- external writes
- destructive operations
- permission or credential changes
- production infrastructure changes
- public publication
- irreversible decisions

Record the answer with `checkpoint_approved`, `checkpoint_rejected`,
`checkpoint_needs_more_info`, or `checkpoint_delegated`.
