"""
tasks.py

Exercise: Task Tracker CLI

Commands:
- python tasks.py add 'Fix login bug'
- python tasks.py done 3
- python tasks.py list
- python tasks.py list --filter done
- python tasks.py delete 3
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


VALID_STATUSES = {"todo", "done"}


@dataclass
class Task:
    id: int
    title: str
    status: str
    created_at: datetime

    def to_dict(self) -> dict[str, Any]:
        # ye is liye use hora hai taake datetime ko JSON me string bana diya jaye
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }

    @staticmethod
    def from_dict(d: dict[str, Any]) -> "Task":
        # ye is liye use hora hai taake JSON data ko wapas Task object me convert kiya ja sake
        return Task(
            id=int(d["id"]),
            title=str(d["title"]),
            status=str(d["status"]),
            created_at=datetime.fromisoformat(d["created_at"]),
        )


class TaskManager:
    def __init__(self, json_path: str | Path = "tasks.json") -> None:
        self.json_path = Path(json_path)
        self.tasks: dict[int, Task] = {}
        self.next_id: int = 1
        self._load()

    def _load(self) -> None:
        if not self.json_path.exists():
            return

        try:
            raw = self.json_path.read_text()
            data = json.loads(raw)
            if not isinstance(data, list):
                raise ValueError("tasks.json must contain a list")

            for item in data:
                task = Task.from_dict(item)
                self.tasks[task.id] = task

            if self.tasks:
                self.next_id = max(self.tasks.keys()) + 1
        except json.JSONDecodeError:
            # corrupt JSON: start fresh (but don't delete the file)
            backup = self.json_path.with_suffix(self.json_path.suffix + ".bak")
            self.json_path.rename(backup)
            self.tasks = {}
            self.next_id = 1
            print(f"Warning: {self.json_path} is corrupt. Backed up to {backup.name}. Starting fresh.")
        except Exception as e:
            backup = self.json_path.with_suffix(self.json_path.suffix + ".bak")
            try:
                self.json_path.rename(backup)
            except Exception:
                pass
            self.tasks = {}
            self.next_id = 1
            print(f"Warning: Could not load tasks ({e}). Starting fresh.")

    def _save(self) -> None:
        # ye is liye use hora hai taake data survives between runs
        payload = [t.to_dict() for t in sorted(self.tasks.values(), key=lambda x: x.id)]
        self.json_path.write_text(json.dumps(payload, indent=2))

    def add_task(self, title: str) -> Task:
        if not title.strip():
            raise ValueError("title must not be empty")

        task = Task(
            id=self.next_id,
            title=title.strip(),
            status="todo",
            created_at=datetime.now(),
        )
        self.tasks[task.id] = task
        self.next_id += 1
        self._save()
        return task

    def complete_task(self, task_id: int) -> Task:
        if task_id not in self.tasks:
            raise KeyError(f"task id {task_id} not found")

        self.tasks[task_id].status = "done"
        self._save()
        return self.tasks[task_id]

    def delete_task(self, task_id: int) -> Task:
        if task_id not in self.tasks:
            raise KeyError(f"task id {task_id} not found")

        removed = self.tasks.pop(task_id)
        self._save()
        return removed

    def list_tasks(self, filter: str | None = None) -> list[Task]:
        tasks = list(self.tasks.values())

        if filter is not None:
            if filter not in VALID_STATUSES:
                raise ValueError("filter must be 'todo' or 'done'")
            tasks = [t for t in tasks if t.status == filter]

        return sorted(tasks, key=lambda x: x.id)


def main() -> None:
    default_file = Path(__file__).with_name("tasks.json")
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    parser.add_argument(
        "--file",
        default=str(default_file),
        help="tasks JSON file path (default: tasks.json)",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("title", type=str)

    p_done = sub.add_parser("done", help="Mark a task as done")
    p_done.add_argument("id", type=int)

    p_del = sub.add_parser("delete", help="Delete a task")
    p_del.add_argument("id", type=int)

    p_list = sub.add_parser("list", help="List tasks")
    p_list.add_argument("--filter", default=None, help="todo or done")

    args = parser.parse_args()
    manager = TaskManager(json_path=args.file)

    try:
        if args.command == "add":
            t = manager.add_task(args.title)
            print(f"Added: {t.id} | {t.title} | {t.status} | {t.created_at.isoformat()}")
        elif args.command == "done":
            t = manager.complete_task(args.id)
            print(f"Completed: {t.id} | {t.title} | {t.status}")
        elif args.command == "delete":
            t = manager.delete_task(args.id)
            print(f"Deleted: {t.id} | {t.title}")
        elif args.command == "list":
            filter_value = args.filter
            tasks = manager.list_tasks(filter=filter_value)
            if not tasks:
                print("No tasks found.")
            for t in tasks:
                print(f"{t.id} | {t.title} | {t.status} | {t.created_at.isoformat()}")
    except KeyError as e:
        print("Error:", e)
        raise SystemExit(1)
    except ValueError as e:
        print("Error:", e)
        raise SystemExit(1)


if __name__ == "__main__":
    main()

