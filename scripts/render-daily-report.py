#!/usr/bin/env python
"""Render Agent Work Ledger events into a Markdown daily report.

Usage:
    python scripts/render-daily-report.py events.jsonl daily-report.md
"""

from __future__ import print_function, unicode_literals

import io
import os
import sys

from ledger_common import VALID_STATES, fold_events, read_events, sorted_tasks, to_text


def md_escape(value):
    return to_text(value).replace("\r", "").strip()


def render_task(task):
    lines = [
        "### {0}: {1}".format(md_escape(task["state"]), md_escape(task["title"])),
        "",
        "- Task ID: `{0}`".format(md_escape(task["task_id"])),
        "- Agent: {0}".format(md_escape(task["agent"])),
        "- Project: {0}".format(md_escape(task["project"]) or "Not specified"),
        "- Outcome: {0}".format(md_escape(task["outcome"]) or "Not specified"),
        "- Next Action: {0}".format(md_escape(task["next_action"]) or "Not recorded"),
        "- Waiting For: {0}".format(md_escape(task["waiting_for"]) or "None"),
        "- Last Update: {0}".format(md_escape(task["last_update"]) or "Unknown"),
        "",
    ]

    if task["progress_log"]:
        lines.append("Progress:")
        for item in task["progress_log"][-3:]:
            lines.append("- {0} {1}".format(md_escape(item.get("ts")), md_escape(item.get("message"))).strip())
        lines.append("")

    if task["evidence"]:
        lines.append("Evidence:")
        for item in task["evidence"]:
            label = md_escape(item.get("label") or item.get("file") or item.get("url") or "Evidence")
            target = md_escape(item.get("file") or item.get("url"))
            lines.append("- [{0}]({1})".format(label, target) if target else "- {0}".format(label))
        lines.append("")

    open_checkpoints = [item for item in task["human_checkpoints"] if not item.get("resolved")]
    if open_checkpoints:
        lines.append("Open Human Checkpoints:")
        for item in open_checkpoints:
            lines.append("- risk={0}: {1}".format(md_escape(item.get("risk") or "unspecified"), md_escape(item.get("message"))))
        lines.append("")

    return "\n".join(lines).rstrip()


def render_report(tasks):
    ordered = sorted_tasks(tasks)
    counts = dict((state, 0) for state in VALID_STATES)
    for task in ordered:
        counts[task["state"]] = counts.get(task["state"], 0) + 1

    lines = [
        "# Agent Work Ledger Daily Report",
        "",
        "This report is generated from the append-only event log.",
        "",
        "## Summary",
        "",
    ]
    for state in ["INBOX", "CLARIFYING", "NEXT", "RUNNING", "WAITING", "REVIEW", "DONE", "CANCELLED"]:
        if counts.get(state):
            lines.append("- {0}: {1}".format(state, counts[state]))

    lines.extend(["", "## Tasks", ""])
    if ordered:
        lines.append("\n\n".join(render_task(task) for task in ordered))
    else:
        lines.append("No tasks found.")
    lines.append("")
    return "\n".join(lines)


def ensure_parent_dir(path):
    parent = os.path.dirname(os.path.abspath(path))
    if parent and not os.path.isdir(parent):
        os.makedirs(parent)


def main(argv):
    if len(argv) != 3:
        print("Usage: render-daily-report.py events.jsonl daily-report.md", file=sys.stderr)
        return 2
    tasks = fold_events(read_events(argv[1]))
    ensure_parent_dir(argv[2])
    with io.open(argv[2], "w", encoding="utf-8") as handle:
        handle.write(render_report(tasks))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
