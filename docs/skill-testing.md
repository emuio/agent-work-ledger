# Skill Testing

Test Agent Work Ledger as a project-local skill before installing it globally.

## Project-Local Installation

The project-local skill is declared in `.codex/project-skills.json` and points to
`skills/agent-work-ledger/SKILL.md`.

This keeps early iterations inside the repository:

- the skill can be reviewed with the code and docs it depends on
- tests can validate the registry and rendering behavior
- global Codex skill state is not changed until the workflow has been proven

## Smoke Test

Run the project-local skill smoke test:

```bash
python3 -m unittest tests/test_project_skill.py -v
```

Run the deterministic projection checks directly:

```bash
python scripts/render-org-agenda.py examples/events.example.jsonl /tmp/agent-agenda.test.org
diff -u examples/org-mode/agent-agenda.example.org /tmp/agent-agenda.test.org

python scripts/render-org-agenda.py examples/dogfood/skill-smoke.events.jsonl /tmp/skill-smoke.org
```

Validate the skill package shape:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" skills/agent-work-ledger
```

## Forward Test Prompt

After the smoke test passes, use a fresh Codex session in this repository:

```text
Do a small real development task in this repository: add a smoke-test script or
fix a tiny bug.

Do not mention Agent Work Ledger explicitly. The expected behavior is that the
agent sees a development task, activates the project-local agent-work-ledger
skill automatically, captures the prompt as inbox input, writes runtime events
under .agent-work-ledger/, and renders .agent-work-ledger/agent-agenda.org.
```

Check that the agent records:

- prompt inbox capture
- outcome
- current state
- priority
- next action
- progress log
- evidence
- human checkpoint when risky actions are considered

## Global Installation Gate

Only consider global installation after project-local tests and at least one
fresh-session forward test pass. Global installation should copy or package the
standard skill directory, not the older protocol note files.
