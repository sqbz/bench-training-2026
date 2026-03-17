## Usage

```bash
python3 pre-training/day-3/tasks.py add "Fix login bug"
python3 pre-training/day-3/tasks.py add "Write unit tests"
python3 pre-training/day-3/tasks.py list
python3 pre-training/day-3/tasks.py list --filter done
python3 pre-training/day-3/tasks.py done 1
python3 pre-training/day-3/tasks.py delete 2
```

## Why a class instead of just functions?

A class keeps the tasks list and the file path together, so every command uses the same state and the same save/load logic. It also gives a clean interface (`add_task`, `complete_task`, `list_tasks`, `delete_task`) that matches the CLI commands. As the app grows (more fields, more commands, different storage), a class-based design is easier to extend without repeating code.

