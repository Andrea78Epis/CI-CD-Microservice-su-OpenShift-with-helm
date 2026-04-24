from flask import Flask, request, jsonify
from db import get_db

app = Flask(__name__)

@app.route("/")
def home():
    return "Task API running"

@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM tasks")
    rows = cur.fetchall()
    return jsonify(rows)

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (name) VALUES (%s)", (data["name"],))
    conn.commit()
    return {"status": "created"}

@app.route("/health")
def health():
    return {"status": "ok"}
