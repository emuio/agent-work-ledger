# Agent Work Ledger Protocol

Agent Work Ledger is an append-only GTD-inspired operating loop for AI agents.
The event log is the source of truth. Org files, dashboards, comments, and daily
reports are projections derived from that log.

## Non-Goals

Agent Work Ledger is not a human GTD application, issue tracker, or replacement
for org-mode, Todoist, Jira, GitHub Issues, or GitLab Issues. Humans should not
edit the GTD files during normal use. It is a protocol for making autonomous
agent work observable.

## Default Activation

Except for simple question answering, agents should activate this loop for
development work: code changes, debugging, review, refactoring, documentation,
research, verification, commits, PRs/MRs, deployments, or remote investigation.

The human prompt is captured as inbox input. The agent classifies the task,
assigns priority, maintains state and next action, records evidence, creates
human checkpoints when needed, and regenerates projections for human observers.

## Task Model

Each task has:

| Field | Purpose |
|---|---|
| `task_id` | Stable machine-readable identifier |
| `title` | Human-readable task name |
| `outcome` | Definition of done |
| `state` | Current lifecycle state |
| `next_action` | Immediate executable next step |
| `waiting_for` | Human, system, CI job, API, or external dependency |
| `evidence` | Files, links, commits, reports, logs, or artifacts |
| `human_checkpoints` | Open or resolved human decisions |
| `progress_log` | Chronological work notes |
| `decision_log` | Decisions and rationale |

## States

```text
INBOX       New goal, not yet clarified
CLARIFYING  Understanding and decomposing the goal
NEXT        Ready with a concrete next action
RUNNING     Actively working
WAITING     Blocked on a person, system, or dependency
REVIEW      Waiting for human review or approval
DONE        Completed with evidence
CANCELLED   Cancelled or no longer relevant
```

Recommended transitions:

```text
INBOX -> CLARIFYING
CLARIFYING -> NEXT
NEXT -> RUNNING
RUNNING -> WAITING
RUNNING -> REVIEW
RUNNING -> DONE
WAITING -> NEXT
REVIEW -> NEXT
REVIEW -> DONE
```

## Event Log

Agents append JSON objects to `.agent-work-ledger/events.jsonl` by default in
consumer projects. They should not treat projected state files as authoritative.

Supported events:

```text
task_created
state_changed
next_action_set
progress_logged
evidence_added
waiting_for_set
human_checkpoint
checkpoint_approved
checkpoint_rejected
checkpoint_needs_more_info
checkpoint_delegated
decision_logged
task_done
task_cancelled
```

Minimum event shape:

```json
{
  "ts": "2026-05-11T10:00:00+09:00",
  "task_id": "ai-governance-001",
  "event": "task_created"
}
```

## Projection Flow

```text
.agent-work-ledger/events.jsonl
    -> materialized task state
    -> .agent-work-ledger/agent-agenda.org
    -> .agent-work-ledger/dashboard.html
    -> GitHub/GitLab comment
    -> .agent-work-ledger/daily-report.md
```

Projection tools may be regenerated at any time. If a projection conflicts with
the event log, the event log wins.

## Completion Rule

A task may move to `DONE` only when the outcome is satisfied or explicitly
reduced, evidence exists, remaining limitations are recorded, and no unresolved
human checkpoint blocks completion.
