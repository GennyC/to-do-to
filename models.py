import mysql.connector
import config


def get_db():
    return mysql.connector.connect(
        host=config.MYSQL_HOST,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        database=config.MYSQL_DB
    )

def get_tasks():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM tasks ORDER BY due_date;")
    tasks = cur.fetchall()
    db.close()
    return tasks

def add_task(title, description, due_date):
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO tasks (title, description, due_date) VALUES (%s,%s,%s)",
        (title, description, due_date)
    )
    db.commit()
    db.close()

def update_status(task_id, status):
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE tasks SET status=%s WHERE id=%s", (status, task_id))
    db.commit()
    db.close()
