import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta

class DB:
    def __init__(self, **kwargs) -> None:
        try:
            self.mydb = mysql.connector.connect(
                host=kwargs["host"],  # Host for MySQL
                user=kwargs["user"],  # MySQL username
                password=kwargs["password"],  # MySQL password
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
        
        # Create the users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                user_telegram_id VARCHAR(255) NOT NULL UNIQUE,
                username VARCHAR(255)
            )
        ''')

        # Create the tasks table with a foreign key to users
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                task_id INT AUTO_INCREMENT PRIMARY KEY,
                task_name VARCHAR(255) NOT NULL,
                description TEXT,
                due_date DATETIME,  -- Stores date and time
                user_id INT,
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
            )
        ''')
        self.mydb.commit()
        print("Tables created successfully.")

    # 2. Insert Data
    def insert_user(self, username, user_telegram_id):
        cursor = self.mydb.cursor()
        cursor.execute('INSERT INTO users (user_telegram_id, username) VALUES (%s, %s)', (user_telegram_id, username,))
        self.mydb.commit()
        print(f"User '{username}' inserted successfully.")

    def insert_task(self, task_name, description, due_date, user_id):
        cursor = self.mydb.cursor()
        cursor.execute('''
            INSERT INTO tasks (task_name, description, due_date, user_id) 
            VALUES (%s, %s, %s, %s)
        ''', (task_name, description, due_date, user_id))
        self.mydb.commit()
        print(f"Task '{task_name}' inserted successfully.")

    # 3. Update Task
    def update_task(self, task_id, task_name=None, description=None, due_date=None, user_id=None):
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

    # 5. Check and Alarm for Due Tasks
    def check_due_tasks(self, time_delta : timedelta = timedelta(hours=1)):
        cursor = self.mydb.cursor(dictionary=True)
        current_time = datetime.now()
        one_hour_from_now = current_time + time_delta
        cursor.execute('''
            SELECT task_id, task_name, description, due_date, user_id
            FROM tasks
            WHERE due_date BETWEEN %s AND %s
        ''', (current_time, one_hour_from_now))

        due_tasks = cursor.fetchall()

        if due_tasks:
            print("Tasks due within the next hour:")
            for task in due_tasks:
                print(f"ALARM! Task '{task['task_name']}' is due at {task['due_date']} for user ID {task['user_id']}.")
        else:
            print("No tasks are due within the next hour.")

    # Close connection
    def close_connection(self):
        if self.mydb.is_connected():
            self.mydb.close()
            print("Connection closed.")

    def user_exists_by_telegram_id(self, telegram_id):
        cursor = self.mydb.cursor()
        cursor.execute('SELECT COUNT(*) FROM users WHERE username = %s', (telegram_id,))
        result = cursor.fetchone()
        return result[0] > 0

# Example Usage

