Day 3: Task Tracker CLI

Files:
- `day-3/tasks.py`
- It saves data into `day-3/tasks.json` (next to `tasks.py`), so tasks stay after you close the script

Usage examples:
```bash
# (Run these from inside `day-3/` so `tasks.py` is found.)
python3 tasks.py add "Fix login bug"
python3 tasks.py list
python3 tasks.py done 3
python3 tasks.py list --filter done
python3 tasks.py delete 3
```

Why I used a class (`TaskManager`) here
Instead of writing only functions, I made `TaskManager` a class because it keeps everything related to tasks in one place:
- It holds the current tasks data in memory (`self.tasks`)
- It knows where the JSON file is (`self.json_path`)
- Its methods (`add_task`, `complete_task`, `delete_task`, `list_tasks`) all use the same stored data

If we used only functions, we would have to pass the tasks data and JSON file path into many functions again and again. The class makes the code cleaner and easier to understand.

