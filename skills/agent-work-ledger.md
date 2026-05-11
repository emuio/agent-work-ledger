# Agent Work Ledger Skill

## Purpose

Enable AI agents to work transparently and autonomously while exposing progress to humans.

This skill is intended for coding agents and research agents that perform multi-step work. It is inspired by GTD, but it is not a human task-management system. It is a work discipline for agents.

## Core Rule

For every complex task, the agent must maintain:

- Outcome
- Current State
- Next Action
- Waiting For
- Evidence
- Progress Log
- Human Checkpoints

The agent must not work silently on multi-step tasks.

## States

Use these states consistently:

```text
INBOX       New goal, not yet clarified
CLARIFYING  Understanding and decomposing the goal
NEXT        Ready with a concrete next action
RUNNING     Actively working
WAITING     Blocked on a person, system, CI job, API, or external dependency
REVIEW      Waiting for human review or approval
DONE        Completed with evidence
CANCELLED   Cancelled or no longer relevant
```

Allowed transitions:

```text
INBOX → CLARIFYING
CLARIFYING → NEXT
NEXT → RUNNING
RUNNING → WAITING
RUNNING → REVIEW
RUNNING → DONE
WAITING → NEXT
REVIEW → NEXT
REVIEW → DONE
```

## Required Task Fields

Every active task should maintain:

| Field | Description |
|---|---|
| `task_id` | Stable identifier for the task |
| `title` | Human-readable task title |
| `outcome` | Definition of done |
| `state` | Current state |
| `next_action` | Immediate executable step |
| `waiting_for` | External dependency, if any |
| `evidence` | Files, links, commits, reports, or logs |
| `human_checkpoints` | Decisions requiring human judgment |
| `progress_log` | Chronological work updates |

## Rules

1. Every active task must always have a concrete Next Action.
2. If no Next Action exists, either create one, mark the task `WAITING`, create a Human Checkpoint, or mark it `DONE` with evidence.
3. If the task depends on another person, system, CI job, API, or external event, move it to `WAITING` and record the dependency.
4. If output is produced, attach Evidence.
5. If human judgment is needed, create a Human Checkpoint and move the task to `REVIEW`.
6. If the task is complete, explain the completion criteria and move it to `DONE`.
7. Do not invent progress. If uncertain, record uncertainty explicitly.
8. Every state change must be appended to the Work Ledger.
9. Every work session must append at least one Progress Log event.
10. High-risk actions require human approval before execution.

## Autonomy Policy

The agent may autonomously perform:

- read-only analysis
- code scanning
- summarization
- draft generation
- report generation
- local file creation for drafts, logs, or reports
- progress logging

The agent must request approval before:

- modifying production code
- opening, merging, closing, or force-updating pull requests
- sending external messages
- changing infrastructure
- changing permissions
- deleting data
- publishing public content
- running destructive commands

## Event Logging

Append events to `events.jsonl` rather than rewriting task state directly.

Recommended events:

- `task_created`
- `state_changed`
- `next_action_set`
- `progress_logged`
- `evidence_added`
- `waiting_for_set`
- `human_checkpoint`
- `checkpoint_approved`
- `checkpoint_rejected`
- `checkpoint_needs_more_info`
- `checkpoint_delegated`
- `decision_logged`
- `task_done`
- `task_cancelled`

## Example Events

```jsonl
{"ts":"2026-05-11T10:00:00+09:00","task_id":"ai-governance-001","event":"task_created","title":"Draft AI coding tool risk list","source":"chat"}
{"ts":"2026-05-11T10:01:00+09:00","task_id":"ai-governance-001","event":"state_changed","from":"INBOX","to":"RUNNING"}
{"ts":"2026-05-11T10:08:00+09:00","task_id":"ai-governance-001","event":"progress_logged","message":"Identified initial risk categories."}
{"ts":"2026-05-11T10:12:00+09:00","task_id":"ai-governance-001","event":"evidence_added","file":"reports/ai-risk-list-v0.1.md"}
{"ts":"2026-05-11T10:15:00+09:00","task_id":"ai-governance-001","event":"human_checkpoint","message":"Confirm whether external SaaS models may access repository code."}
```

## Completion Criteria

A task may be marked `DONE` only when:

1. The outcome has been satisfied, or the scope has been explicitly reduced.
2. Evidence exists.
3. Remaining assumptions or limitations are recorded.
4. No pending Human Checkpoint remains unresolved.

## Reporting Style

When reporting to humans, summarize:

- Current state
- Last progress
- Next action
- Blockers
- Evidence
- Required human decision

Keep reports factual. Avoid overstating progress.
