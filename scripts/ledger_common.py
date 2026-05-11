#!/usr/bin/env python
"""Shared helpers for Agent Work Ledger projection scripts.

The module intentionally uses only the Python standard library and keeps syntax
compatible with both Python 2.7 and Python 3.x because many systems still map
the `python` command to Python 2.
"""

from __future__ import print_function, unicode_literals

import io
import json
import re

try:
    text_type = unicode
except NameError:  # pragma: no cover - Python 3
    text_type = str


VALID_STATES = set([
    "INBOX",
    "CLARIFYING",
    "NEXT",
    "RUNNING",
    "WAITING",
    "REVIEW",
    "DONE",
    "CANCELLED",
])

CHECKPOINT_RESOLUTION_EVENTS = set([
    "checkpoint_approved",
    "checkpoint_rejected",
    "checkpoint_needs_more_info",
    "checkpoint_delegated",
])


def to_text(value, default=""):
    if value is None:
        return default
    if isinstance(value, text_type):
        return value
    return text_type(value)


def tagify(value):
    value = to_text(value).strip().lower()
    value = re.sub(r"[^a-z0-9_@#%:-]+", "-", value)
    value = value.strip("-:")
    return value or "general"


def new_task(task_id):
    return {
        "task_id": to_text(task_id),
        "title": "Untitled task",
        "state": "INBOX",
        "priority": "B",
        "agent": "agent",
        "project": "",
        "project_tag": "general",
        "outcome": "",
        "next_action": "",
        "waiting_for": "",
        "evidence": [],
        "human_checkpoints": [],
        "progress_log": [],
        "decision_log": [],
        "last_update": "",
    }


def read_events(path):
    events = []
    with io.open(path, "r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except ValueError as exc:
                raise SystemExit("Invalid JSON on line {0}: {1}".format(line_number, exc))
            if "task_id" not in event or "event" not in event:
                raise SystemExit("Missing required fields on line {0}: task_id and event".format(line_number))
            events.append(event)
    return events


def get_task(tasks, task_id):
    task_id = to_text(task_id)
    if task_id not in tasks:
        tasks[task_id] = new_task(task_id)
    return tasks[task_id]


def mark_checkpoint_resolved(task, checkpoint_id):
    if checkpoint_id:
        for checkpoint in task["human_checkpoints"]:
            if checkpoint.get("checkpoint_id") == checkpoint_id:
                checkpoint["resolved"] = True
                return
    for checkpoint in reversed(task["human_checkpoints"]):
        if not checkpoint.get("resolved"):
            checkpoint["resolved"] = True
            return


def apply_event(tasks, event):
    task = get_task(tasks, event["task_id"])
    event_type = to_text(event["event"])
    ts = to_text(event.get("ts"))
    task["last_update"] = ts or task["last_update"]

    if event_type == "task_created":
        task["title"] = to_text(event.get("title"), task["title"])
        task["outcome"] = to_text(event.get("outcome"), task["outcome"])
        task["agent"] = to_text(event.get("agent"), task["agent"])
        task["project"] = to_text(event.get("project"), task["project"])
        task["project_tag"] = tagify(event.get("project_tag", task["project"] or task["project_tag"]))
        state = to_text(event.get("state"), task["state"])
        if state in VALID_STATES:
            task["state"] = state
        task["progress_log"].append({"ts": ts, "message": "Task created: {0}".format(task["title"])})
        return

    if event_type == "state_changed":
        new_state = to_text(event.get("to", event.get("state")))
        if new_state in VALID_STATES:
            task["state"] = new_state
        return

    if event_type == "next_action_set":
        task["next_action"] = to_text(event.get("next_action", event.get("message", task["next_action"])))
        return

    if event_type == "progress_logged":
        message = to_text(event.get("message"))
        if message:
            task["progress_log"].append({"ts": ts, "message": message})
        return

    if event_type == "evidence_added":
        task["evidence"].append({
            "ts": ts,
            "label": to_text(event.get("label", event.get("file", event.get("url", "Evidence")))),
            "file": to_text(event.get("file")),
            "url": to_text(event.get("url")),
        })
        return

    if event_type == "waiting_for_set":
        task["waiting_for"] = to_text(event.get("waiting_for", event.get("message", task["waiting_for"])))
        if task["waiting_for"]:
            task["state"] = "WAITING"
        return

    if event_type == "human_checkpoint":
        message = to_text(event.get("message"))
        task["human_checkpoints"].append({
            "checkpoint_id": to_text(event.get("checkpoint_id")),
            "ts": ts,
            "message": message,
            "risk": to_text(event.get("risk")),
            "options": event.get("options", []),
            "recommended_option": to_text(event.get("recommended_option")),
            "resolved": False,
        })
        if message:
            task["next_action"] = message
        task["state"] = "REVIEW"
        return

    if event_type in CHECKPOINT_RESOLUTION_EVENTS:
        task["decision_log"].append({
            "ts": ts,
            "decision": to_text(event.get("decision", event_type)),
            "decided_by": to_text(event.get("decided_by", "human")),
        })
        mark_checkpoint_resolved(task, to_text(event.get("checkpoint_id")))
        return

    if event_type == "decision_logged":
        task["decision_log"].append({
            "ts": ts,
            "decision": to_text(event.get("decision", event.get("message"))),
            "decided_by": to_text(event.get("decided_by", "agent")),
        })
        return

    if event_type == "task_done":
        task["state"] = "DONE"
        task["next_action"] = ""
        task["waiting_for"] = ""
        task["progress_log"].append({"ts": ts, "message": to_text(event.get("message", "Task completed."))})
        return

    if event_type == "task_cancelled":
        task["state"] = "CANCELLED"
        task["next_action"] = ""
        task["waiting_for"] = ""
        task["progress_log"].append({"ts": ts, "message": to_text(event.get("message", "Task cancelled."))})
        return


def fold_events(events):
    tasks = {}
    for event in events:
        apply_event(tasks, event)
    return tasks


def sorted_tasks(tasks):
    terminal = set(["DONE", "CANCELLED"])
    return sorted(
        tasks.values(),
        key=lambda task: (task["state"] in terminal, task["last_update"], task["task_id"]),
    )
