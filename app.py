from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS equipment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        type TEXT,
        usage INTEGER,
        maintenance_date TEXT
    )''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        type_ = request.form['type']
        usage = request.form['usage']
        date = request.form['maintenance_date']
        c.execute("INSERT INTO equipment (name, type, usage, maintenance_date) VALUES (?, ?, ?, ?)",
                  (name, type_, usage, date))
        conn.commit()
        return redirect('/')

    c.execute("SELECT * FROM equipment")
    rows = c.fetchall()
    conn.close()

    alert_rows = []
    for row in rows:
        last_date = datetime.strptime(row[4], "%Y-%m-%d")
        days = (datetime.today() - last_date).days
        if days > 30:
            status = " Due"
        elif days > 20:
            status = " Soon"
        else:
            status = "OK"
        alert_rows.append((*row, status))

    return render_template('index.html', equipment=alert_rows)

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

