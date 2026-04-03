from flask import Flask, request, jsonify
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Database configuration
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Sundara@123',
    database='TASK_MANAGER'
)

cursor = db.cursor()
@app.route('/')
def home():
    return "Backend is running!"

@app.route('/add_task', methods=['POST'])
def add_task():
    try:
        data = request.json

        Title = data['Title']
        Description = data['Description']
        Due_Date = datetime.strptime(data['Due_Date'], "%d-%m-%y").strftime("%Y-%m-%d")
        Status = data['Status']
        User_ID = data['User_ID']

        query = "INSERT INTO TASK (Title, Description, Due_Date, Status, User_ID) VALUES (%s, %s, %s, %s, %s)"
        values = (Title, Description, Due_Date, Status, User_ID)
        cursor.execute(query, values)
        db.commit()

        return jsonify({"message": "Task added successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_tasks', methods=['GET'])
def get_tasks():
    try:
        cursor.execute("SELECT * FROM task")
        rows = cursor.fetchall()

        tasks = []
        for row in rows:
            task = {
                "id": row[0],
                "Title": row[1],
                "Description": row[2],
                "Due_Date": str(row[3]),
                "Status": row[4],
                "User_ID": row[5]
            }
            tasks.append(task)

        return jsonify(task)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/delete_task/<int:id>', methods=['DELETE'])
def delete_task(id):
    try:
    
        cursor.execute("DELETE FROM task WHERE id = %s", (id,))
        db.commit()

        return jsonify({"message": "Task deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500 
    
@app.route('/update_task/<int:id>', methods=['PUT'])
def update_task(id):
    try:
        data = request.json
        Status = data['Status']

        cursor.execute("UPDATE task SET Status = %s WHERE id = %s", (Status, id))
        db.commit()

        return jsonify({"message": "Task updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}),500

if __name__ == '__main__':
    app.run(debug=True)

