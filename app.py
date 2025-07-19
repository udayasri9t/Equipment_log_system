from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# 🔧 Create table if it doesn't exist
def init_db():
    db_path = 'log.db'
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS equipment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            model TEXT NOT NULL,
            location TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')

    # Check if table is empty
    c.execute("SELECT COUNT(*) FROM equipment")
    count = c.fetchone()[0]

    if count == 0:
        print("Inserting default data...")
        default_data = [
            ("Drill Press", "DP-450", "Factory A", "2025-07-18"),
            ("CNC Machine", "CNC-X21", "Workshop 3", "2025-07-18"),
            ("Welder", "WELD-32", "Maintenance", "2025-07-17"),
            ("Lathe", "LATHE-M2", "Factory B", "2025-07-16"),
            ("Forklift", "FLK-900", "Warehouse", "2025-07-15")
        ]
        c.executemany("INSERT INTO equipment (name, model, location, date) VALUES (?, ?, ?, ?)", default_data)
        conn.commit()
        print("Default data inserted!")
    else:
        print("Database already has data. Skipping insert.")

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
