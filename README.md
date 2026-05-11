# Agent Work Ledger

[English](README.md) | [Simplified Chinese](README_CN.md)

> Agents should not work in the dark.

**Agent Work Ledger** is a lightweight, GTD-inspired operating loop for AI agents. It lets coding agents and research agents automatically capture development prompts as inbox items, track outcomes, next actions, blockers, evidence, decisions, and human checkpoints, then project that state into org-agenda, dashboards, GitHub/GitLab comments, or daily reports.

This project is **not** a human GTD app. It does not replace Emacs org-mode, Todoist, Jira, GitHub Issues, or GitLab Issues.

Instead, it defines a transparent work protocol for agents:

```text
Human prompt
        ↓
Agent Work Ledger inbox capture
        ↓
events.jsonl
        ↓
State projector
        ↓
agent-agenda.org / dashboard.html / issue comment / daily report
```

`events.jsonl` is the source of truth. Everything else is a projection that can
be regenerated. Humans observe the projections; agents own the GTD files.

## Why

Modern coding agents can analyze, write, refactor, and review code, but their work often remains opaque:

- What is the agent doing now?
- What is the next concrete action?
- What is blocked?
- What evidence or output has been produced?
- What needs human approval?
- Why did the agent decide to stop?

Agent Work Ledger makes this visible.

## Default Agent Loop

Agent Work Ledger is meant to be automatic for development work. Except for
simple question answering, an agent should use it for code changes, debugging,
review, refactoring, documentation, research, verification, commits, PRs/MRs,
deployments, and remote investigation.

The agent should:

- capture the human prompt as inbox input
- classify the task and assign priority
- maintain one current next action
- update state as work moves through `RUNNING`, `WAITING`, `REVIEW`, and `DONE`
- record evidence for files, commands, logs, commits, reports, and links
- create human checkpoints for risky or judgment-heavy actions
- regenerate agenda/dashboard/report projections for human observation

## Core Concepts

Every non-trivial agent task should maintain:

| Field | Meaning |
|---|---|
| Outcome | What “done” means |
| State | Current task state, such as `RUNNING`, `WAITING`, or `REVIEW` |
| Next Action | The immediate executable step |
| Waiting For | A human, system, CI job, API, or external dependency |
| Evidence | Files, reports, commits, logs, links, or other proof of work |
| Human Checkpoints | Decisions requiring human judgment or approval |
| Progress Log | Chronological updates |
| Decision Log | Important decisions and rationale |

## Event Types

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

## Minimal Example

`events.jsonl`:

```jsonl
{"ts":"2026-05-11T10:00:00+09:00","task_id":"ai-governance-001","event":"task_created","title":"Draft AI coding tool risk list","source":"chat"}
{"ts":"2026-05-11T10:01:00+09:00","task_id":"ai-governance-001","event":"state_changed","from":"INBOX","to":"RUNNING"}
{"ts":"2026-05-11T10:08:00+09:00","task_id":"ai-governance-001","event":"progress_logged","message":"Identified risks: code leakage, over-broad permissions, missing audit logs, CI pollution, vendor compliance."}
{"ts":"2026-05-11T10:12:00+09:00","task_id":"ai-governance-001","event":"evidence_added","file":"reports/ai-risk-list-v0.1.md"}
{"ts":"2026-05-11T10:15:00+09:00","task_id":"ai-governance-001","event":"human_checkpoint","message":"Confirm whether external SaaS models may access repository code."}
{"ts":"2026-05-11T10:16:00+09:00","task_id":"ai-governance-001","event":"state_changed","from":"RUNNING","to":"REVIEW"}
```

Projected `agent-agenda.org`:

```org
* REVIEW [#B] Agent: Draft AI coding tool risk list :agent:ai-governance:
:PROPERTIES:
:TASK_ID: ai-governance-001
:STATUS: REVIEW
:NEXT_ACTION: Confirm whether external SaaS models may access repository code.
:EVIDENCE: file:reports/ai-risk-list-v0.1.md
:END:
```

## Repository Layout

```text
skills/                 Agent-facing work protocol prompts
ledger/                 JSON schemas for event and state records
scripts/                Lightweight renderers and utilities
examples/               Codex, Claude Code, org-mode, and GitLab/GitHub examples
docs/                   Protocol, autonomy, audit, and roadmap docs
.agent-work-ledger/     Runtime ledger files generated inside consumer projects
```

## Quick Start

In a consumer project, install or copy the project-local skill and gitignore the
runtime ledger directory:

```text
.codex/project-skills.json
skills/agent-work-ledger/SKILL.md
.agent-work-ledger/
```

For development tasks, the agent should append work events to:

```text
.agent-work-ledger/events.jsonl
```

Then render:

```bash
python scripts/render-org-agenda.py .agent-work-ledger/events.jsonl .agent-work-ledger/agent-agenda.org
```

Optional projections:

```bash
python scripts/render-dashboard.py .agent-work-ledger/events.jsonl .agent-work-ledger/dashboard.html
python scripts/render-daily-report.py .agent-work-ledger/events.jsonl .agent-work-ledger/daily-report.md
```

Add the generated file to Emacs org-agenda:

```elisp
(add-to-list 'org-agenda-files "/path/to/project/.agent-work-ledger/agent-agenda.org")
```

## Autonomy Policy

Agents may perform low-risk work autonomously:

- read-only analysis
- code scanning
- summarization
- draft generation
- report generation
- local progress logging

Agents must request human approval before:

- modifying production code
- opening, merging, or closing pull requests
- sending external messages
- changing infrastructure
- changing permissions
- deleting data
- publishing public content

## Supported Agents

The first version focuses on Codex and Claude Code. The protocol is intentionally
runtime-neutral, so other coding agents and research agents can append the same
event records.

## Status

Early prototype. The first milestone is a minimal protocol, JSONL event log, org-agenda renderer, and examples for coding agents such as Codex and Claude Code.

## Roadmap

- v0.1: protocol, event schema, org-agenda renderer, coding agent examples
- v0.2: dashboard and daily report renderers
- v0.3: MCP server and human checkpoint API
- v0.4: multi-agent support and stronger audit model
- v1.0: stable protocol and enterprise-ready projections
