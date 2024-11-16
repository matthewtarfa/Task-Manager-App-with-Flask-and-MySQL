from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database connection function
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="db",
            user="root",
            password="example",
            database="task_db"
        )
        return connection
    except Error as e:
        return str(e)

# Route for the home page
@app.route('/')
def home():
    return "Welcome to the Task Management API! Use /tasks to interact with tasks."

# Route to create a new task
@app.route('/tasks', methods=['POST'])
def add_task():
    task_description = request.json.get('description')
    if not task_description:
        return jsonify({"error": "Task description is required"}), 400

    connection = get_db_connection()
    if isinstance(connection, str):  # If connection fails
        return jsonify({"error": connection}), 500

    cursor = connection.cursor()
    cursor.execute("INSERT INTO tasks (description) VALUES (%s)", (task_description,))
    connection.commit()
    task_id = cursor.lastrowid
    cursor.close()
    connection.close()

    return jsonify({"message": "Task added successfully", "task_id": task_id}), 201

# Route to get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    connection = get_db_connection()
    if isinstance(connection, str):  # If connection fails
        return jsonify({"error": connection}), 500

    cursor = connection.cursor()
    cursor.execute("SELECT id, description FROM tasks")
    tasks = cursor.fetchall()
    cursor.close()
    connection.close()

    task_list = [{"id": task[0], "description": task[1]} for task in tasks]
    return jsonify(task_list), 200

# Route to delete a task by ID
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    connection = get_db_connection()
    if isinstance(connection, str):  # If connection fails
        return jsonify({"error": connection}), 500

    cursor = connection.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Task deleted successfully"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0')

