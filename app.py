from flask import Flask, render_template, request, redirect, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "expense_secret"   # required for flash


# function to calculate total 
def calculate_total(data):
    total = 0
    for e in data:
        total += e[2]
    return total


# create database (run once on start)
conn = sqlite3.connect("database.db")
cursor = conn.cursor()
cursor.execute("DROP TABLE expenses;")
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses(
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT,
amount INTEGER NOT NULL CHECK(amount > 0)
)
""")

conn.commit()
conn.close()


# home route 
@app.route("/")
def home():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses")
    data = cursor.fetchall()

    conn.close()

    total = calculate_total(data)

    return render_template("index.html", expenses=data, total=total)


# add route
@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"].title()
    amount = int(request.form["amount"])

    # ✅ Backend validation (BEST WAY)
    if amount <= 0:
        flash("❌ Negative amount not allowed")
        return redirect("/")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO expenses (title, amount) VALUES (?, ?)",
            (title, amount)
        )
        conn.commit()
        flash("✅ Expense Added")

    except sqlite3.IntegrityError:
        flash("❌ Amount must be positive")

    conn.close()
    return redirect("/")


# delete route
@app.route("/delete/<id>")
def delete(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM expenses WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    flash("🗑 Expense Deleted")
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)