from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_PATH = "/tmp/data.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return "Flask + SQLite running on OpenShift"

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    rows = cur.fetchall()
    conn.close()
    return jsonify(rows)

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (name) VALUES (?)", (data["name"],))
    conn.commit()
    conn.close()
    return {"status": "created"}

# 🚀 INIT DB QUI (FIX OPENSHIFT + FLASK 3.x)
init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
