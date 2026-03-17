import argparse
import json
import os
import sys
from datetime import datetime


class Task:
    VALID_STATUSES = ("todo", "done")

    def __init__(self, task_id, title, status, created_at):
        self.id = int(task_id)
        self.title = str(title)
        self.status = status
        self.created_at = created_at

    @staticmethod
    def now_iso():
        return datetime.now().isoformat(timespec="seconds")

    @classmethod
    def next_id(cls, tasks):
        if not tasks:
            return 1
        return max(t.id for t in tasks) + 1

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data):
        task_id = data.get("id")
        title = data.get("title")
        status = data.get("status", "todo")
        created_at = data.get("created_at")
        if status not in cls.VALID_STATUSES:
            status = "todo"
        if not created_at:
            created_at = cls.now_iso()
        return cls(task_id, title, status, created_at)


class BaseTaskManager:
    def add_task(self, title):
        raise NotImplementedError

    def complete_task(self, task_id):
        raise NotImplementedError

    def list_tasks(self, status_filter=None):
        raise NotImplementedError

    def delete_task(self, task_id):
        raise NotImplementedError


class TaskManager(BaseTaskManager):
    def __init__(self, json_path):
        self.json_path = json_path
        self.tasks = []
        self.load()

    def load(self):
        if not os.path.exists(self.json_path):
            self.tasks = []
            return

        try:
            with open(self.json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            backup = self.json_path + ".corrupt." + datetime.now().strftime("%Y%m%d%H%M%S")
            try:
                os.replace(self.json_path, backup)
            except OSError:
                pass
            self.tasks = []
            print("Warning: tasks.json was corrupt. Started with an empty list.", file=sys.stderr)
            return
        except OSError as e:
            self.tasks = []
            print(f"Warning: could not read tasks.json ({e}). Started with an empty list.", file=sys.stderr)
            return

        if not isinstance(data, list):
            self.tasks = []
            return

        loaded = []
        for item in data:
            if isinstance(item, dict):
                loaded.append(Task.from_dict(item))
        self.tasks = loaded

    def save(self):
        data = [t.to_dict() for t in self.tasks]
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def add_task(self, title):
        task_id = Task.next_id(self.tasks)
        task = Task(task_id, title, "todo", Task.now_iso())
        self.tasks.append(task)
        self.save()
        return task

    def _find_task(self, task_id):
        task_id = int(task_id)
        for t in self.tasks:
            if t.id == task_id:
                return t
        return None

    def complete_task(self, task_id):
        task = self._find_task(task_id)
        if not task:
            return None
        task.status = "done"
        self.save()
        return task

    def delete_task(self, task_id):
        task = self._find_task(task_id)
        if not task:
            return False
        self.tasks = [t for t in self.tasks if t.id != task.id]
        self.save()
        return True

    def list_tasks(self, status_filter=None):
        if status_filter in Task.VALID_STATUSES:
            return [t for t in self.tasks if t.status == status_filter]
        return list(self.tasks)


def print_tasks(tasks):
    if not tasks:
        print("No tasks found.")
        return

    print("id | status | created_at           | title")
    for t in tasks:
        print(f"{t.id:>2} | {t.status:<6} | {t.created_at:<19} | {t.title}")


def build_parser():
    parser = argparse.ArgumentParser(prog="tasks.py")
    sub = parser.add_subparsers(dest="command", required=True)

    add_p = sub.add_parser("add")
    add_p.add_argument("title")

    done_p = sub.add_parser("done")
    done_p.add_argument("id", type=int)

    del_p = sub.add_parser("delete")
    del_p.add_argument("id", type=int)

    list_p = sub.add_parser("list")
    list_p.add_argument("--filter", choices=["todo", "done"], default=None)

    return parser


def main():
    json_path = os.path.join(os.path.dirname(__file__), "tasks.json")
    manager = TaskManager(json_path)
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "add":
        task = manager.add_task(args.title)
        print(f"Added task {task.id}: {task.title}")
        return 0

    if args.command == "done":
        task = manager.complete_task(args.id)
        if not task:
            print(f"Error: no task found with id {args.id}", file=sys.stderr)
            return 1
        print(f"Completed task {task.id}: {task.title}")
        return 0

    if args.command == "delete":
        ok = manager.delete_task(args.id)
        if not ok:
            print(f"Error: no task found with id {args.id}", file=sys.stderr)
            return 1
        print(f"Deleted task {args.id}")
        return 0

    if args.command == "list":
        tasks = manager.list_tasks(args.filter)
        print_tasks(tasks)
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())

