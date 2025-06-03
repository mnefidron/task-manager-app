import sqlite3
from datetime import datetime

def create_task(title, description, deadline, priority, status, assignees):
    conn = sqlite3.connect('task_manager.db')
    c = conn.cursor()
    
    c.execute("INSERT INTO tasks (title, description, deadline, priority, status, assignees) VALUES (?, ?, ?, ?, ?, ?)",
              (title, description, deadline, priority, status, ",".join(assignees)))
    
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect('task_manager.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    
    conn.close()
    return tasks

def update_task_status(task_id, new_status):
    conn = sqlite3.connect('task_manager.db')
    c = conn.cursor()
    
    c.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
    
    conn.commit()
    conn.close()

def update_task(task_id, title, description, deadline, priority, status, assignees):
    conn = sqlite3.connect('task_manager.db')
    c = conn.cursor()
    
    c.execute("UPDATE tasks SET title = ?, description = ?, deadline = ?, priority = ?, status = ?, assignees = ? WHERE id = ?",
              (title, description, deadline, priority, status, ",".join(assignees), task_id))
    
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect('task_manager.db')
    c = conn.cursor()
    
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    
    conn.commit()
    conn.close()