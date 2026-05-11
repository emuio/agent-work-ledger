# Org Agenda Bridge Skill

## Purpose

Project Agent Work Ledger state into an org-mode file that humans can view with Emacs org-agenda.

The bridge should not replace a human's existing GTD system. It creates a separate agent-facing agenda file, usually named `agent-agenda.org`.

## Output Principles

1. Use normal org headings.
2. Use the task state as the org TODO keyword.
3. Prefix titles with `Agent:` so agent work is visually distinct.
4. Use tags such as `:agent:`, project tags, and state tags.
5. Store machine-readable metadata in the `PROPERTIES` drawer.
6. Keep the agenda line short; put details in child sections.

## Recommended Heading Format

```org
* REVIEW [#B] Agent: Draft AI coding tool risk list :agent:ai-governance:
:PROPERTIES:
:TASK_ID: ai-governance-001
:AGENT: codex
:PROJECT: AI Coding Governance
:STATUS: REVIEW
:NEXT_ACTION: Confirm whether external SaaS models may access repository code.
:WAITING_FOR: emuio
:EVIDENCE: file:reports/ai-risk-list-v0.1.md
:LAST_UPDATE: 2026-05-11T10:16:00+09:00
:END:

** Outcome
Create a reviewable risk list for AI coding tool adoption.

** Current Next Action
Confirm whether external SaaS models may access repository code.

** Progress Log
- 2026-05-11 10:08 Identified initial risk categories.

** Evidence
- [[file:reports/ai-risk-list-v0.1.md][AI coding tool risk list v0.1]]

** Human Checkpoints
- Confirm whether external SaaS models may access repository code.
```

## TODO Keywords

Recommended org-mode TODO keywords:

```elisp
(setq org-todo-keywords
      '((sequence "INBOX(i)" "CLARIFYING(c)" "NEXT(n)" "RUNNING(r)" "WAITING(w)" "REVIEW(v)" "|" "DONE(d)" "CANCELLED(x)")))
```

## Agenda Files

Use a separate file for agent work:

```elisp
(add-to-list 'org-agenda-files "~/org/agent/agent-agenda.org")
```

## Projection Rules

- `task_created` creates or updates a heading.
- `state_changed` updates the org TODO keyword and `STATUS` property.
- `next_action_set` updates `NEXT_ACTION` and the `Current Next Action` section.
- `waiting_for_set` updates `WAITING_FOR` and may set state to `WAITING`.
- `progress_logged` appends to the `Progress Log` section.
- `evidence_added` appends to the `Evidence` section and updates the `EVIDENCE` property.
- `human_checkpoint` appends to `Human Checkpoints` and may set state to `REVIEW`.
- `checkpoint_approved`, `checkpoint_rejected`, `checkpoint_needs_more_info`, and `checkpoint_delegated` mark a checkpoint resolved and append to the `Decision Log` section.
- `task_done` sets state to `DONE`.
- `task_cancelled` sets state to `CANCELLED`.

## Human-Friendly Labels

For non-Emacs users, the same ledger can be projected to a web dashboard with labels:

| Agent State | Human Label |
|---|---|
| INBOX | New |
| CLARIFYING | Clarifying |
| NEXT | Ready |
| RUNNING | In progress |
| WAITING | Blocked |
| REVIEW | Needs review |
| DONE | Done |
| CANCELLED | Cancelled |
