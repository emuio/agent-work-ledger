# Org Agenda Bridge

The org-agenda bridge projects agent work into a separate org-mode file. It does
not replace a human's existing GTD system. It gives humans a familiar agenda
surface for monitoring autonomous agent work.

## Generate the File

```bash
python scripts/render-org-agenda.py examples/events.example.jsonl /tmp/agent-agenda.org
```

## Add to Emacs

```elisp
(add-to-list 'org-agenda-files "~/org/agent/agent-agenda.org")

(setq org-todo-keywords
      '((sequence "INBOX(i)" "CLARIFYING(c)" "NEXT(n)" "RUNNING(r)" "WAITING(w)" "REVIEW(v)" "|" "DONE(d)" "CANCELLED(x)")))
```

## Projection Rules

| Event | Org Effect |
|---|---|
| `task_created` | Create or update task heading |
| `state_changed` | Update TODO keyword and `STATUS` property |
| `next_action_set` | Update `NEXT_ACTION` and current next action section |
| `waiting_for_set` | Update `WAITING_FOR`; usually move to `WAITING` |
| `progress_logged` | Append progress entry |
| `evidence_added` | Append evidence link |
| `human_checkpoint` | Append checkpoint and move to `REVIEW` |
| `checkpoint_*` | Record decision and mark checkpoint resolved |
| `task_done` | Move to `DONE` |
| `task_cancelled` | Move to `CANCELLED` |

## Heading Shape

```org
* REVIEW [#B] Agent: Draft AI coding tool risk list :agent:ai-governance:
:PROPERTIES:
:TASK_ID: ai-governance-001
:AGENT: codex
:PROJECT: AI Coding Governance
:STATUS: REVIEW
:NEXT_ACTION: Confirm whether external SaaS models may access repository code.
:WAITING_FOR:
:LAST_UPDATE: 2026-05-11T10:16:00+09:00
:END:
```

The heading is intentionally compact. Details belong in child sections such as
Outcome, Current Next Action, Progress Log, Evidence, and Human Checkpoints.
