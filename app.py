from flask import Flask, render_template, request, redirect, url_for
import sqlite3
app = Flask(__name__)
def get_db_connection():
    conn = sqlite3.connect("todos.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    todos = conn.execute(
        "SELECT * FROM todos ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return render_template("index.html", todos=todos)

@app.route("/add", methods=["GET", "POST"])
def add_todo():
    if request.method == "POST":
        title = request.form["title"]
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO todos (title) VALUES (?)",
            (title,)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("add.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_todo(id):
    conn = get_db_connection()
    todo = conn.execute(
        "SELECT * FROM todos WHERE id = ?",
        (id,)
    ).fetchone()
    if request.method == "POST":
        title = request.form["title"]
        conn.execute(
            "UPDATE todos SET title = ? WHERE id = ?",
            (title, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    conn.close()
    return render_template("edit.html", todo=todo)

@app.route("/delete/<int:id>")
def delete_todo(id):
    conn = get_db_connection()
    conn.execute(
        "DELETE FROM todos WHERE id = ?",
        (id,)
    )
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/complete/<int:id>", methods=["POST"])
def complete_todo(id):
    conn = get_db_connection()
    conn.execute(
        """
        UPDATE todos
        SET completed = CASE
            WHEN completed = 0 THEN 1
            ELSE 0
        END
        WHERE id = ?
        """,
        (id,)
    )
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)