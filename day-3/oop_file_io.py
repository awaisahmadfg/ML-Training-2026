"""
oop_file_io.py

OOP + File I/O examples.

Covers:
- Creating classes
- Storing data in objects
- Reading/writing JSON (file I/O)
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Note:
    title: str
    body: str

    def to_dict(self) -> dict[str, Any]:
        # ye is liye use hora hai taake object ko JSON-friendly format me convert kiya ja sake
        return {"title": self.title, "body": self.body}

    @staticmethod
    def from_dict(d: dict[str, Any]) -> "Note":
        # ye is liye use hora hai taake dictionary se Note object ban jaye
        return Note(title=d["title"], body=d["body"])


def save_notes(path: str | Path, notes: list[Note]) -> None:
    p = Path(path)
    payload = [n.to_dict() for n in notes]
    p.write_text(json.dumps(payload, indent=2))


def load_notes(path: str | Path) -> list[Note]:
    p = Path(path)
    if not p.exists():
        return []

    raw = p.read_text()
    data = json.loads(raw)  # if JSON is wrong, it will raise (this file is just a learning example)
    return [Note.from_dict(item) for item in data]


def main() -> None:
    path = Path("notes.json")

    notes = [
        Note("Hello", "This is my first note."),
        Note("Python", "Classes make code easier to manage."),
    ]

    save_notes(path, notes)
    loaded = load_notes(path)

    print("Saved and loaded notes:")
    for n in loaded:
        print("-", n.title, "|", n.body)


if __name__ == "__main__":
    main()

