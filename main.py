import json
import sys
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as file:
        return json.load(file)

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

def add_task(description):
    tasks = load_tasks()
    task_id = len(tasks) + 1
    now = datetime.now().isoformat()
    task = {"id": task_id, "description": description, "status": "todo", "createdAt": now, "updatedAt": now}
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added: {description}")

def update_task(task_id, description):
    tasks = load_tasks()

    if not tasks:
        print("The task list is empty. Please add some tasks.")
        return
    
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = description
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print("Task updated.")
            return
    print("Task not found.")

def delete_task(task_id):
    tasks = load_tasks()
    task_exists = any(task["id"] == task_id for task in tasks)

    if not task_exists:
        print(f"Task with ID {task_id} does not exist.")
        return
    
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)
    print("Task deleted.")

def change_status(task_id, status):
    if status not in ["todo", "in-progress", "done"]:
        print("Invalid status. Use 'todo', 'in-progress', or 'done'.")
        return
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task status updated to {status}.")
            return
    print("Task not found.")

def list_tasks(filter_status=None):
    tasks = load_tasks()

    if not tasks:
        print("the task list is empty.Please add some tasks.")
        return
    
    filtered_tasks = [task for task in tasks if filter_status is None or task["status"] == filter_status]

    if not filtered_tasks:
        print("No tasks found with this filter")
        return
    
    for task in filtered_tasks:
        print(task)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <command> [args]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "add" and len(sys.argv) > 2:
        add_task(" ".join(sys.argv[2:]))
    elif command == "update" and len(sys.argv) > 3:
        update_task(int(sys.argv[2]), " ".join(sys.argv[3:]))
    elif command == "delete" and len(sys.argv) > 2:
        delete_task(int(sys.argv[2]))
    elif command == "status" and len(sys.argv) > 3:
        change_status(int(sys.argv[2]), sys.argv[3])
    elif command == "list":
        list_tasks()
    elif command == "list-done":
        list_tasks("done")
    elif command == "list-not-done":
        list_tasks("todo")
    elif command == "list-in-progress":
        list_tasks("in-progress")
    else:
        print("Invalid command or missing arguments.")
