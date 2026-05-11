---
name: agent-work-ledger
description: Default Agent GTD operating loop for development work. Use automatically for non-trivial coding, debugging, review, refactoring, documentation, research, verification, commit, PR, or deployment tasks except simple question answering. Captures the human prompt as inbox input, maintains agent-owned work state, and renders observable org-agenda/dashboard/report projections.
---

# Agent Work Ledger

## Purpose

Use this as the default Agent GTD operating loop for development work. Humans
give prompts and observe projections; the agent owns the ledger, state changes,
classification, priority, and org output.

Do not wait for the user to ask for this skill. Use it automatically for
development tasks unless the request is a simple question that can be answered
directly without code changes, investigation, review, or verification.

## Runtime Files

Use `.agent-work-ledger/` for runtime state in a normal project:

```text
.agent-work-ledger/events.jsonl
.agent-work-ledger/agent-agenda.org
.agent-work-ledger/dashboard.html
.agent-work-ledger/daily-report.md
```

This directory should be gitignored by default. The event log is the source of
truth; org-agenda, dashboard, and reports are projections.

## Operating Loop

1. **Inbox capture**: Treat the human prompt as inbox input. Create or update a
   task with `task_created`, preserving the prompt source in `source` or
   `metadata`.
2. **Clarify and classify**: Infer task type, project, priority, outcome, and
   initial state. Use `CLARIFYING` when the prompt is ambiguous; otherwise move
   to `NEXT` or `RUNNING`.
3. **Next action discipline**: Every active task must have one concrete
   `next_action`. If no next action exists, move the task to `WAITING`,
   `REVIEW`, `DONE`, or `CANCELLED`.
4. **Progress logging**: Append `progress_logged` at meaningful milestones:
   investigation started, root cause found, files changed, verification run,
   failure encountered, external wait started, review requested, or work
   completed.
5. **Evidence tracking**: Append `evidence_added` for files, commands, logs,
   commits, reports, PRs/MRs, review comments, or generated artifacts.
6. **Human checkpoints**: If the next action requires human judgment or a risky
   external write, append `human_checkpoint`, move to `REVIEW`, and pause that
   action until a checkpoint resolution event is recorded.
7. **Projection refresh**: After meaningful state changes, regenerate
   `.agent-work-ledger/agent-agenda.org`. Generate dashboard/report projections
   when useful for humans.

## State and Priority

Use these states:

```text
INBOX CLARIFYING NEXT RUNNING WAITING REVIEW DONE CANCELLED
```

Use priority conservatively:

- `A`: urgent, blocked human workflow, production issue, or explicit user
  priority.
- `B`: normal development task.
- `C`: cleanup, exploration, or optional follow-up.

## Event Quick Reference

Use these events:

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

## Rendering

Render the ledger with project scripts when present:

```bash
python scripts/render-org-agenda.py .agent-work-ledger/events.jsonl .agent-work-ledger/agent-agenda.org
python scripts/render-dashboard.py .agent-work-ledger/events.jsonl .agent-work-ledger/dashboard.html
python scripts/render-daily-report.py .agent-work-ledger/events.jsonl .agent-work-ledger/daily-report.md
```

The scripts must keep using only the Python standard library.

## References

Read these only when more detail is needed:

- `../agent-work-ledger.md` for the full agent work discipline.
- `../human-checkpoints.md` for checkpoint creation and resolution rules.
- `../org-agenda-bridge.md` for org projection rules.
- `../../docs/protocol.md` for the protocol contract.
