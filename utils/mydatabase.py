import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta

class DB:
    def __init__(self, **kwargs) -> None:
        try:
            self.mydb = mysql.connector.connect(
                host=kwargs["host"],  # Make sure to pass host argument when initializing
                user=kwargs["user"],  # MySQL username as `user`
                password=kwargs["password"],  # MySQL password as `password`
                database=kwargs.get("database")  # Optional: database name
            )
            if self.mydb.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error: '{e}'")

    def print_db(self):
        print(self.mydb)

    # 1. Create Tables
    def create_tables(self):
        cursor = self.mydb.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255),
                user_telegram_id VARCHAR(255) UNIQUE
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                task_id INT AUTO_INCREMENT PRIMARY KEY,
                task_name VARCHAR(255) NOT NULL,
                description TEXT,
                due_date DATE,
                due_hour DATE,
                user_id INT,
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
            )
        ''')
        self.mydb.commit()
        print("Tables created successfully.")

    # 2. Insert Data
    def insert_user(self, username):
        cursor = self.mydb.cursor()
        cursor.execute('INSERT INTO users (username) VALUES (%s)', (username,))
        self.mydb.commit()
        print(f"User '{username}' inserted successfully.")

    def insert_task(self, task_name, description, due_date, due_hour, user_id):
        cursor = self.mydb.cursor()
        cursor.execute('''
            INSERT INTO tasks (task_name, description, due_date, due_hour, user_id) 
            VALUES (%s, %s, %s, %s, %s)
        ''', (task_name, description, due_date, due_hour, user_id))
        self.mydb.commit()
        print(f"Task '{task_name}' inserted successfully.")

    # 3. Update Data
    def update_task(self, task_id, task_name=None, description=None, due_date=None, due_hour=None, user_id=None):
        cursor = self.mydb.cursor()
        query = "UPDATE tasks SET "
        params = []
        if task_name:
            query += "task_name = %s, "
            params.append(task_name)
        if description:
            query += "description = %s, "
            params.append(description)
        if due_date:
            query += "due_date = %s, "
            params.append(due_date)
        if due_hour:
            query += "due_hour = %s, "
            params.append(due_hour)
        if user_id:
            query += "user_id = %s, "
            params.append(user_id)
        query = query.rstrip(', ') + " WHERE task_id = %s"
        params.append(task_id)

        cursor.execute(query, params)
        self.mydb.commit()
        print(f"Task with ID {task_id} updated successfully.")

    # 4. Delete Data
    def delete_task(self, task_id):
        cursor = self.mydb.cursor()
        cursor.execute('DELETE FROM tasks WHERE task_id = %s', (task_id,))
        self.mydb.commit()
        print(f"Task with ID {task_id} deleted successfully.")

    def delete_user(self, user_id):
        cursor = self.mydb.cursor()
        cursor.execute('DELETE FROM users WHERE user_id = %s', (user_id,))
        self.mydb.commit()
        print(f"User with ID {user_id} deleted successfully.")

    # Close connection
    def close_connection(self):
        if self.mydb.is_connected():
            self.mydb.close()
            print("Connection closed.")

    # 5. Check Due Tasks
    def check_due_tasks(self):
        cursor = self.mydb.cursor(dictionary=True)
        current_time = datetime.now()
        one_hour_from_now = current_time + timedelta(days=2, hours=1)
        print(current_time)
        print(one_hour_from_now)

        cursor.execute('''
            SELECT task_id, task_name, description, due_date, due_hour, user_id
            FROM tasks
            WHERE due_date BETWEEN %s AND %s AND due_hour BETWEEN %s AND %s
        ''', (current_time.day, one_hour_from_now.day, current_time.hour, one_hour_from_now.hour))

        due_tasks = cursor.fetchall()
        print(due_tasks)

        if due_tasks:
            print("Tasks due within the next hour:")
            for task in due_tasks:
                print(f"ALARM! Task '{task['task_name']}' is due at {task['due_date']} for user ID {task['user_id']}.")
        else:
            print("No tasks are due within the next hour.")

# Example Usage
db = DB(host="localhost", user="psbot", password="psbot2024@", database="psbot")
db.print_db()
db.create_tables()
print("created tables")
#db.insert_user("BOB")
db.insert_task("Complete Report", "Finalize the quarterly report", "2024-10-29", "15-56-00" , 1)

task_name = "Submit Project Proposal"
description = "Prepare and submit the project proposal document"
due_date = "2024-10-28 16:56:00"  # Due date in 'YYYY-MM-DD HH:MM:SS' format
user_id = 1  # Replace with the actual user_id for JohnDoe

# # # Insert task
db.insert_task(task_name, description, due_date, user_id)
db.check_due_tasks()

db.close_connection()
