# Agent Work Ledger Project Instructions

## Repository Language Policy

- Use English as the primary language for repository metadata, commit messages,
  code comments, schemas, scripts, issue templates, and public protocol docs.
- Keep commit messages short and in English. Prefer a one-line subject unless a
  human explicitly asks for a longer commit body.
- Maintain `README.md` as the canonical English entry point.
- Maintain `README_CN.md` as the Simplified Chinese entry point for domestic
  users. Keep it aligned with `README.md` when changing user-facing behavior.

## Agent Work Policy

- Preserve the protocol boundary: `events.jsonl` is the source of truth;
  org-agenda files, dashboards, GitHub/GitLab comments, and Markdown reports are
  projections.
- Except for simple question answering, use the project-local
  `agent-work-ledger` skill for development tasks: code changes, debugging,
  review, refactoring, documentation, research, verification, commits, PRs, MRs,
  deployments, or remote investigation.
- Treat the human prompt as inbox input. The agent owns `.agent-work-ledger/`
  runtime files, task state, priority, next actions, and projections; humans
  observe these files rather than editing them.
- Prefer the project-local skill registry in `.codex/project-skills.json` before
  considering global installation.
- Test project-local skills inside this repository before copying or installing
  them globally.
- Prefer small, auditable changes. Avoid unrelated rewrites.
- Use only Python standard library code in `scripts/` unless the project
  explicitly introduces dependency management.
- Keep generated files such as `__pycache__/` and `*.pyc` out of commits.

## About This File

- `AGENTS.md` is a versioned project-level instruction file for Codex and other
  compatible coding agents.
- Commit this file when it contains public project conventions that should be
  shared by all contributors and agent sessions.
- Do not use this file for private local memory, credentials, machine-specific
  paths, unpublished business context, or personal preferences that should not be
  public. Keep those in local agent memory or untracked local notes instead.
