from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# function to calculate total 
def calculate_total(data):
        total = 0
        for e in data:
           total += e[2]
        return total

# create table
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses(
id INTEGER PRIMARY KEY ,
title TEXT,
amount INTEGER
)
""")

conn.commit()
conn.close()

#home route 
@app.route("/")
def home():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses")
    data = cursor.fetchall()

    conn.close()

    total = calculate_total(data)

    return render_template("index.html", expenses=data, total=total)

#add route
@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"].title()
    amount = request.form["amount"]
    amount = int(amount)

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO expenses (title, amount) VALUES (?, ?)",
        (title, amount)
    )

    conn.commit()
    conn.close()

    return redirect("/")

#delete route

@app.route("/delete/<id>")
def delete(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM expenses WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
