# Autonomy Levels

Agent Work Ledger separates observable work from permission to act. Agents can
record progress at any level, but higher-risk actions require explicit human
checkpoints.

## Level 0: Observe

Allowed without approval:

- read files and logs
- inspect issues, commits, and CI output
- summarize current state
- append progress events

## Level 1: Draft

Allowed without approval:

- draft plans, reports, comments, and patches
- generate local projections from the event log
- create evidence files that do not affect production systems

## Level 2: Local Change

Usually allowed when the user has requested implementation:

- edit local files in the working tree
- run local tests and scripts
- create local commits

The agent should record evidence and move to `REVIEW` when a human decision is
needed before publication.

## Level 3: External Change

Requires a human checkpoint unless already authorized by the current request:

- push branches
- open, update, merge, or close pull requests
- post GitHub, GitLab, Slack, Feishu, or WeCom messages
- trigger deployments or remote jobs

## Level 4: High-Risk Change

Always requires explicit approval:

- change production infrastructure
- modify credentials, secrets, or permissions
- delete data
- publish public-facing content
- run destructive commands
- bypass policy gates

## Checkpoint Format

Each checkpoint should state the decision, options, recommendation, risk, and
consequence of no answer. The agent should stop the risky action until a
resolution event is recorded.
