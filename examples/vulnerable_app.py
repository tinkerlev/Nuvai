"""
File: vulnerable_app.py

Description:
Example vulnerable Python application for demonstration purposes with Nuvai.
Includes intentional security flaws such as code injection, exposed secrets,
debug configurations, and insecure transport, designed to test Nuvai's detection engine.
"""

from flask import Flask, request, render_template
import os
import sqlite3

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'supersecretkey123'

@app.route("/login", methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    user = cursor.fetchone()
    return f"Welcome {username}" if user else "Login failed"

@app.route("/run")
def run():
    code = request.args.get("code")
    return str(eval(code))

@app.route("/data")
def data():
    user_input = request.args.get("info")
    return render_template("data.html", content=user_input)

@app.route("/ping")
def ping():
    host = request.args.get("host")
    os.system(f"ping -c 1 {host}")
    return "Ping sent"

@app.route("/profile/<id>")
def profile(id):
    return f"Profile page for user {id}"

if __name__ == '__main__':
    app.run()