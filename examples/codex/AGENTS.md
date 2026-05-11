# Codex Agent Work Ledger Example

Use Agent Work Ledger for multi-step work in this repository.

## Rules

- Maintain Outcome, Current State, Next Action, Waiting For, Evidence, Progress Log, and Human Checkpoints.
- Append events to `events.jsonl`; do not treat generated projections as source of truth.
- Add evidence when producing files, commits, reports, logs, or review output.
- Create a human checkpoint before high-risk external actions such as pushing, merging, changing infrastructure, deleting data, or publishing public content.
- Keep updates factual and auditable.

## State Keywords

Use these states:

```text
INBOX CLARIFYING NEXT RUNNING WAITING REVIEW DONE CANCELLED
```

## Example Event

```json
{"ts":"2026-05-11T10:00:00+09:00","task_id":"example-001","event":"progress_logged","message":"Inspected failing CI job and collected the log URL.","agent":"codex"}
```
