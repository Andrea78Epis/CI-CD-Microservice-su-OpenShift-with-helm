from flask import Flask, request, jsonify
import sqlite3, os

SWAGGER_ENABLED = os.getenv("SWAGGER_ENABLED", "false") == "true"
SWAGGER_PATH = os.getenv("SWAGGER_PATH", "/swagger")

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
    return jsonify([
    {"id": r[0], "name": r[1]} for r in rows
    ])

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (name) VALUES (?)", (data["name"],))
    conn.commit()
    conn.close()
    return {"status": "created"}
    
@app.route("/ui")
def ui():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    rows = cur.fetchall()
    conn.close()

    html = "<h1>Task Dashboard</h1><ul>"

    for r in rows:
        html += f"<li>{r[0]} - {r[1]}</li>"

    html += "</ul>"
    return html

# 🚀 INIT DB QUI (FIX OPENSHIFT + FLASK 3.x)
init_db()

@app.route(SWAGGER_PATH)
def swagger():
    if not SWAGGER_ENABLED:
        return "Swagger disabled", 404

    return """
    <html>
        <head>
            <title>Swagger UI</title>
        </head>
        <body>
            <h1>Swagger UI</h1>
            <p>API Documentation placeholder</p>

            <h3>Endpoints</h3>
            <ul>
                <li>GET /health</li>
                <li>GET /tasks</li>
                <li>POST /tasks</li>
                <li>GET /ui</li>
            </ul>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
