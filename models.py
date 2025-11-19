import mysql.connector
import config
from datetime import datetime, timedelta
from collections import defaultdict
from werkzeug.security import generate_password_hash, check_password_hash


def get_db():
    return mysql.connector.connect(
        host=config.MYSQL_HOST,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        database=config.MYSQL_DB
    )

# User authentication functions
def create_user(nombre, email, password):
    db = get_db()
    cur = db.cursor()
    hashed_password = generate_password_hash(password)
    
    try:
        cur.execute(
            "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
            (nombre, email, hashed_password)
        )
        db.commit()
        return True
    except mysql.connector.IntegrityError:
        return False  # Email already exists
    finally:
        db.close()

def get_user_by_email(email):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
    user = cur.fetchone()
    db.close()
    return user

def verify_user(email, password):
    user = get_user_by_email(email)
    if user and check_password_hash(user['password'], password):
        return user
    return None

# Keep all your existing task functions below...
# Update all task functions to include user_id filtering

def get_tasks(user_id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM tasks WHERE user_id = %s ORDER BY due_date;", (user_id,))
    tasks = cur.fetchall()
    db.close()
    return tasks

def get_tasks_by_status(status, user_id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM tasks WHERE status = %s AND user_id = %s ORDER BY due_date;", (status, user_id))
    tasks = cur.fetchall()
    db.close()
    return tasks

def get_tasks_due_this_week(user_id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    
    # Calculate start and end of current week (Monday to Sunday)
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    cur.execute("""
        SELECT * FROM tasks 
        WHERE due_date BETWEEN %s AND %s AND user_id = %s
        ORDER BY due_date;
    """, (start_of_week, end_of_week, user_id))
    tasks = cur.fetchall()
    db.close()
    return tasks

def get_tasks_due_this_month(user_id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    
    # Calculate start and end of current month
    today = datetime.now().date()
    start_of_month = today.replace(day=1)
    next_month = today.replace(day=28) + timedelta(days=4)  # Move to next month
    end_of_month = next_month - timedelta(days=next_month.day)
    
    cur.execute("""
        SELECT * FROM tasks 
        WHERE due_date BETWEEN %s AND %s AND user_id = %s
        ORDER BY due_date;
    """, (start_of_month, end_of_month, user_id))
    tasks = cur.fetchall()
    db.close()
    return tasks

def get_tasks_grouped_by_month(status, user_id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM tasks WHERE status = %s AND user_id = %s ORDER BY due_date;", (status, user_id))
    tasks = cur.fetchall()
    db.close()
    
    # Group tasks by month and year with proper date objects for sorting
    grouped_tasks = {}
    
    for task in tasks:
        if task['due_date']:
            # Create a proper date key for sorting
            date_key = task['due_date'].replace(day=1)  # Use first day of month for grouping
            month_year_display = task['due_date'].strftime('%B %Y')
            
            if date_key not in grouped_tasks:
                grouped_tasks[date_key] = {
                    'display_name': month_year_display,
                    'tasks': []
                }
            grouped_tasks[date_key]['tasks'].append(task)
        else:
            # Handle tasks with no due date
            if 'no_date' not in grouped_tasks:
                grouped_tasks['no_date'] = {
                    'display_name': 'No Due Date',
                    'tasks': []
                }
            grouped_tasks['no_date']['tasks'].append(task)
    
    # Sort by date (oldest first)
    sorted_groups = {}
    
    # Separate dated and undated tasks
    dated_items = [(key, value) for key, value in grouped_tasks.items() if key != 'no_date']
    undated_items = [(key, value) for key, value in grouped_tasks.items() if key == 'no_date']
    
    # Sort dated items chronologically (oldest first)
    dated_items.sort(key=lambda x: x[0])
    
    # Combine: dated tasks first (oldest to newest), then undated
    for key, value in dated_items:
        sorted_groups[value['display_name']] = value['tasks']
    
    for key, value in undated_items:
        sorted_groups[value['display_name']] = value['tasks']
    
    return sorted_groups

def add_task(title, description, due_date, user_id):
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO tasks (title, description, due_date, user_id) VALUES (%s,%s,%s,%s)",
        (title, description, due_date, user_id)
    )
    db.commit()
    db.close()

def update_status(task_id, user_id, status):
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE tasks SET status=%s WHERE id=%s AND user_id=%s", (status, task_id, user_id))
    db.commit()
    db.close()
# Add these functions to your models.py

def update_user_name(user_id, new_name):
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute(
            "UPDATE usuarios SET nombre = %s WHERE id = %s",
            (new_name, user_id)
        )
        db.commit()
        return True
    except Exception as e:
        print(f"Error updating name: {e}")
        return False
    finally:
        db.close()

def update_user_password(user_id, new_password):
    db = get_db()
    cur = db.cursor()
    try:
        hashed_password = generate_password_hash(new_password)
        cur.execute(
            "UPDATE usuarios SET password = %s WHERE id = %s",
            (hashed_password, user_id)
        )
        db.commit()
        return True
    except Exception as e:
        print(f"Error updating password: {e}")
        return False
    finally:
        db.close()

def get_user_by_id(user_id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT id, nombre, email, creado_en FROM usuarios WHERE id = %s", (user_id,))
    user = cur.fetchone()
    db.close()
    return user

def delete_task(task_id, user_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM tasks WHERE id=%s AND user_id=%s", (task_id, user_id))
    db.commit()
    affected_rows = cur.rowcount
    db.close()
    return affected_rows > 0