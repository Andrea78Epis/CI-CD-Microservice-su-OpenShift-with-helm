from flask import Flask, request
from flask_restx import Api, Resource, fields
import sqlite3

app = Flask(__name__)

api = Api(
    app,
    version="1.0",
    title="DevOps Tasks API",
    description="Flask + SQLite + OpenShift demo"
)

ns = api.namespace("tasks", description="Task operations")

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


task_model = api.model("Task", {
    "name": fields.String(required=True, description="Task name")
})


@ns.route("/")
class TaskList(Resource):

    def get(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT * FROM tasks")
        rows = cur.fetchall()
        conn.close()

        return [{"id": r[0], "name": r[1]} for r in rows]

    @ns.expect(task_model)
    def post(self):
        data = api.payload

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("INSERT INTO tasks (name) VALUES (?)", (data["name"],))
        conn.commit()
        conn.close()

        return {"status": "created"}, 201


@api.route("/health")
class Health(Resource):
    def get(self):
        return {"status": "ok"}


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
