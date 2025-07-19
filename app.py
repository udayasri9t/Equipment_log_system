from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# 🔧 Create table if it doesn't exist
def init_db():
    conn = sqlite3.connect('log.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS equipment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            model TEXT NOT NULL,
            location TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# 🔁 Homepage: View logs
@app.route('/')
def index():
    conn = sqlite3.connect('log.db')
    c = conn.cursor()
    c.execute("SELECT * FROM equipment")
    rows = c.fetchall()
    conn.close()
    return render_template('index.html', data=rows)

# ➕ Add log
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    model = request.form['model']
    location = request.form['location']
    date = request.form['date']

    conn = sqlite3.connect('log.db')
    c = conn.cursor()
    c.execute("INSERT INTO equipment (name, model, location, date) VALUES (?, ?, ?, ?)",
              (name, model, location, date))
    conn.commit()
    conn.close()
    return redirect('/')

# 🔁 Create table on startup
init_db()

if __name__ == '__main__':
   import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # default to 10000 for local testing
    app.run(host='0.0.0.0', port=port)
