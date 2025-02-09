import os
from flask import Flask, render_template, request, redirect, flash
import mysql.connector
from datetime import datetime

# Get the absolute path of the `src/` directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define Flask app with explicit paths
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "../templates"),  # Adjust path
    static_folder=os.path.join(BASE_DIR, "../static")  # Adjust path
)

app.secret_key = "secret_key"

# MySQL Database Configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="flask_db"
)
cursor = db.cursor()

# Ensure users table exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        create_time DATE NOT NULL
    )
""")
db.commit()

# Route: Fetch and display users
@app.route('/')
def index():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return render_template('index.html', users=users)

# Route: Add a new user
@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name']
    create_time = datetime.now().strftime("%Y-%m-%d")

    if name:
        cursor.execute("INSERT INTO users (name, create_time) VALUES (%s, %s)", (name, create_time))
        db.commit()
        flash("User added successfully!", "success")
    else:
        flash("Name cannot be empty!", "error")

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)