# Human Checkpoints Skill

## Purpose

Define when an AI agent must pause for human review or approval.

A Human Checkpoint is a structured request for human judgment. It should be clear, actionable, and tied to a specific task.

## When to Create a Human Checkpoint

Create a checkpoint when the agent needs to:

- change production code or infrastructure
- create, merge, close, or modify a pull request
- send an external message
- access sensitive data
- change permissions or credentials
- delete data
- publish public content
- make an irreversible decision
- choose between materially different strategies
- proceed despite uncertainty or incomplete information

## Checkpoint Format

Each checkpoint should include:

- Question
- Context
- Options
- Recommended option, if any
- Risk
- Consequence of no decision

Example:

```json
{
  "ts": "2026-05-11T10:15:00+09:00",
  "task_id": "ai-governance-001",
  "event": "human_checkpoint",
  "message": "Confirm whether external SaaS models may access repository code.",
  "options": ["allow", "deny", "allow only redacted snippets"],
  "recommended_option": "allow only redacted snippets",
  "risk": "high",
  "consequence_if_unanswered": "The agent will keep the task in REVIEW and avoid sending code to external models."
}
```

## State Behavior

When a Human Checkpoint is created:

1. Append a `human_checkpoint` event.
2. Move the task to `REVIEW` unless it is already `WAITING` for a different dependency.
3. Update `next_action` to the human decision required.
4. Stop executing high-risk actions until the checkpoint is resolved.

## Resolution Events

Use one of these events:

- `checkpoint_approved`
- `checkpoint_rejected`
- `checkpoint_needs_more_info`
- `checkpoint_delegated`

Example:

```json
{
  "ts": "2026-05-11T11:00:00+09:00",
  "task_id": "ai-governance-001",
  "event": "checkpoint_approved",
  "checkpoint_id": "cp-001",
  "decision": "allow only redacted snippets",
  "decided_by": "emuio"
}
```

## Rule of Thumb

If an action would surprise a responsible human, create a Human Checkpoint first.
