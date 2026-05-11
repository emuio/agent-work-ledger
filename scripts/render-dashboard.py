#!/usr/bin/env python
"""Render Agent Work Ledger events into a static HTML dashboard.

Usage:
    python scripts/render-dashboard.py events.jsonl dashboard.html
"""

from __future__ import print_function, unicode_literals

import io
import os
import sys

from ledger_common import fold_events, read_events, sorted_tasks, to_text

try:
    from html import escape as html_escape
except ImportError:  # pragma: no cover - Python 2
    from cgi import escape as html_escape


def esc(value):
    return html_escape(to_text(value), quote=True)


def latest_progress(task):
    if not task["progress_log"]:
        return ""
    item = task["progress_log"][-1]
    return "{0} {1}".format(to_text(item.get("ts")), to_text(item.get("message"))).strip()


def render_dashboard(tasks):
    rows = []
    for task in sorted_tasks(tasks):
        evidence_count = len(task["evidence"])
        open_checkpoints = len([item for item in task["human_checkpoints"] if not item.get("resolved")])
        rows.append(
            "<tr>"
            "<td><span class=\"state state-{state}\">{state}</span></td>"
            "<td>{title}<div class=\"meta\">{task_id}</div></td>"
            "<td>{next_action}</td>"
            "<td>{waiting_for}</td>"
            "<td>{evidence_count}</td>"
            "<td>{open_checkpoints}</td>"
            "<td>{last_update}</td>"
            "</tr>".format(
                state=esc(task["state"]),
                title=esc(task["title"]),
                task_id=esc(task["task_id"]),
                next_action=esc(task["next_action"] or latest_progress(task)),
                waiting_for=esc(task["waiting_for"]),
                evidence_count=evidence_count,
                open_checkpoints=open_checkpoints,
                last_update=esc(task["last_update"]),
            )
        )

    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Agent Work Ledger Dashboard</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 32px; color: #202124; }}
    h1 {{ font-size: 24px; margin-bottom: 8px; }}
    p {{ color: #5f6368; }}
    table {{ border-collapse: collapse; width: 100%; margin-top: 24px; }}
    th, td {{ border-bottom: 1px solid #e0e0e0; padding: 10px 12px; text-align: left; vertical-align: top; }}
    th {{ font-size: 12px; color: #5f6368; text-transform: uppercase; letter-spacing: 0.04em; }}
    .meta {{ color: #777; font-size: 12px; margin-top: 4px; }}
    .state {{ display: inline-block; min-width: 92px; border-radius: 4px; padding: 3px 6px; font-size: 12px; font-weight: 600; text-align: center; }}
    .state-RUNNING {{ background: #e8f0fe; color: #174ea6; }}
    .state-REVIEW {{ background: #fef7e0; color: #b06000; }}
    .state-WAITING {{ background: #fce8e6; color: #a50e0e; }}
    .state-DONE {{ background: #e6f4ea; color: #137333; }}
    .state-CANCELLED {{ background: #f1f3f4; color: #5f6368; }}
  </style>
</head>
<body>
  <h1>Agent Work Ledger Dashboard</h1>
  <p>Static projection generated from the append-only event log.</p>
  <table>
    <thead>
      <tr>
        <th>State</th>
        <th>Task</th>
        <th>Next Action</th>
        <th>Waiting For</th>
        <th>Evidence</th>
        <th>Open Checks</th>
        <th>Last Update</th>
      </tr>
    </thead>
    <tbody>
      {rows}
    </tbody>
  </table>
</body>
</html>
""".format(rows="\n      ".join(rows))


def ensure_parent_dir(path):
    parent = os.path.dirname(os.path.abspath(path))
    if parent and not os.path.isdir(parent):
        os.makedirs(parent)


def main(argv):
    if len(argv) != 3:
        print("Usage: render-dashboard.py events.jsonl dashboard.html", file=sys.stderr)
        return 2
    tasks = fold_events(read_events(argv[1]))
    ensure_parent_dir(argv[2])
    with io.open(argv[2], "w", encoding="utf-8") as handle:
        handle.write(render_dashboard(tasks))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
