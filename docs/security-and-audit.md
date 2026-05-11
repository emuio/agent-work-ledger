# Security and Audit

Agent Work Ledger makes agent activity auditable, but it is not a security
boundary by itself. Treat the ledger as evidence and control metadata, not as an
authorization system.

## Audit Principles

- Append events instead of silently rewriting state.
- Preserve timestamps, agent identities, and evidence links.
- Keep human checkpoint decisions explicit.
- Treat generated projections as disposable views.
- Prefer repository commits or immutable storage for important ledger records.

## Sensitive Data

Agents should not write secrets, private keys, tokens, passwords, or raw
customer data into ledger events. Store sensitive evidence in the approved secure
system and link only to the authorized record.

Recommended event fields for sensitive evidence:

```json
{
  "event": "evidence_added",
  "label": "Production error log excerpt",
  "url": "https://internal.example/audit/log-123",
  "metadata": {
    "contains_sensitive_data": true,
    "access_control": "internal-audit"
  }
}
```

## Human Checkpoints

High-risk actions require a `human_checkpoint` event before execution. The
resolution event should record who decided and what was approved or rejected.

Resolution events:

```text
checkpoint_approved
checkpoint_rejected
checkpoint_needs_more_info
checkpoint_delegated
```

## Tamper Evidence

For stronger auditability, teams can:

- commit `events.jsonl` to Git
- sign release commits or tags
- mirror ledger events into append-only object storage
- include commit hashes in `evidence_added` events
- export daily reports to an immutable audit archive

## Operational Boundary

The ledger can show that an agent requested approval, waited, and acted after a
decision. Enforcement still belongs in the surrounding systems: repository
permissions, CI policies, deployment gates, secrets managers, and identity
providers.
