#!/usr/bin/env python
"""Render Agent Work Ledger events into an org-agenda compatible file.

Usage:
    python scripts/render-org-agenda.py events.jsonl agent-agenda.org

The script intentionally uses only the Python standard library.
"""

from __future__ import print_function, unicode_literals

import io
import os
import sys

from ledger_common import fold_events, read_events, sorted_tasks, tagify, to_text


def org_escape(value):
    return to_text(value).replace("\r", "").strip()


def render_evidence_item(item):
    label = org_escape(item.get("label") or item.get("file") or item.get("url") or "Evidence")
    file_value = to_text(item.get("file"))
    url_value = to_text(item.get("url"))
    if file_value:
        return "- [[file:{0}][{1}]]".format(org_escape(file_value), label)
    if url_value:
        return "- [[{0}][{1}]]".format(org_escape(url_value), label)
    return "- {0}".format(label)


def property_line(name, value):
    value = org_escape(value)
    if value:
        return ":{0}: {1}".format(name, value)
    return ":{0}:".format(name)


def current_next_action_text(task):
    if task["next_action"]:
        return org_escape(task["next_action"])
    if task["state"] == "DONE":
        return "No further action; task is DONE."
    if task["state"] == "CANCELLED":
        return "No further action; task is CANCELLED."
    return "No next action recorded."


def render_task(task):
    tags = ":agent:{0}:".format(tagify(task["project_tag"]))
    lines = ["* {0} [#{1}] Agent: {2} {3}".format(task["state"], task["priority"], org_escape(task["title"]), tags)]
    lines.extend([
        ":PROPERTIES:",
        property_line("TASK_ID", task["task_id"]),
        property_line("AGENT", task["agent"]),
        property_line("PROJECT", task["project"]),
        property_line("STATUS", task["state"]),
        property_line("NEXT_ACTION", task["next_action"]),
        property_line("WAITING_FOR", task["waiting_for"]),
        property_line("LAST_UPDATE", task["last_update"]),
        ":END:",
        "",
        "** Outcome",
        org_escape(task["outcome"]) or "Not specified.",
        "",
        "** Current Next Action",
        current_next_action_text(task),
        "",
        "** Progress Log",
    ])

    if task["progress_log"]:
        for item in task["progress_log"]:
            line = "- {0} {1}".format(org_escape(item.get("ts")), org_escape(item.get("message"))).strip()
            lines.append(line)
    else:
        lines.append("- No progress logged yet.")

    lines.extend(["", "** Evidence"])
    if task["evidence"]:
        lines.extend(render_evidence_item(item) for item in task["evidence"])
    else:
        lines.append("- No evidence recorded yet.")

    lines.extend(["", "** Human Checkpoints"])
    if task["human_checkpoints"]:
        for checkpoint in task["human_checkpoints"]:
            status = "resolved" if checkpoint.get("resolved") else "open"
            risk = checkpoint.get("risk") or "unspecified"
            lines.append(
                "- [{0}] {1} risk={2}: {3}".format(
                    status,
                    org_escape(checkpoint.get("ts")),
                    org_escape(risk),
                    org_escape(checkpoint.get("message")),
                )
            )
    else:
        lines.append("- No human checkpoints recorded.")

    if task["decision_log"]:
        lines.extend(["", "** Decision Log"])
        for decision in task["decision_log"]:
            lines.append(
                "- {0} {1}: {2}".format(
                    org_escape(decision.get("ts")),
                    org_escape(decision.get("decided_by")),
                    org_escape(decision.get("decision")),
                )
            )

    return "\n".join(lines).rstrip() + "\n"


def render_org(tasks):
    header = [
        "#+TITLE: Agent Work Ledger Agenda",
        "#+STARTUP: overview",
        "#+TODO: INBOX(i) CLARIFYING(c) NEXT(n) RUNNING(r) WAITING(w) REVIEW(v) | DONE(d) CANCELLED(x)",
    ]
    return "\n".join(header) + "\n\n" + "\n".join(render_task(task) for task in sorted_tasks(tasks))


def ensure_parent_dir(path):
    parent = os.path.dirname(os.path.abspath(path))
    if parent and not os.path.isdir(parent):
        os.makedirs(parent)


def main(argv):
    if len(argv) != 3:
        print("Usage: render-org-agenda.py events.jsonl agent-agenda.org", file=sys.stderr)
        return 2

    events = read_events(argv[1])
    tasks = fold_events(events)
    ensure_parent_dir(argv[2])
    with io.open(argv[2], "w", encoding="utf-8") as handle:
        handle.write(render_org(tasks))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
