<<<<<<< HEAD
from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

# -------------------------
# DATABASE SETUP
# -------------------------

def init_user_db():
    conn = sqlite3.connect('health_tracker.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

def init_db():
    conn = sqlite3.connect('health_tracker.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS health_data (
                    id INTEGER PRIMARY KEY,
                    date TEXT,
                    weight REAL,
                    steps INTEGER,
                    water INTEGER,
                    user_id INTEGER
                )''')
    conn.commit()
    conn.close()

# -------------------------
# ROUTES
# -------------------------

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.context_processor
def inject_theme():
    theme = request.cookies.get("theme", "minimalist")
    return dict(theme=theme)

@app.route('/theme/<name>')
def switch_theme(name):
    allowed = ["minimalist", "tailwind", "bootstrap", "dark"]
    if name in allowed:
        resp = redirect(request.referrer or '/')
        resp.set_cookie("theme", name)
        return resp
    return "Invalid theme", 400

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('health_tracker.db')
    c = conn.cursor()

    c.execute("SELECT date, weight, steps, water FROM health_data ORDER BY date")
    rows = c.fetchall()
    conn.close()

    if not rows:
        return render_template(
            "dashboard.html",
            dates=[],
            weights=[],
            steps=[],
            water=[],
            total_entries=0,
            avg_weight=0,
            avg_steps=0,
            avg_water=0
        )

    dates = [row[0] for row in rows]
    weights = [row[1] for row in rows]
    steps = [row[2] for row in rows]
    water = [row[3] for row in rows]

    total_entries = len(rows)
    avg_weight = round(sum(weights) / total_entries, 1)
    avg_steps = int(sum(steps) / total_entries)
    avg_water = int(sum(water) / total_entries)

    return render_template(
        "dashboard.html",
        dates=dates,
        weights=weights,
        steps=steps,
        water=water,
        total_entries=total_entries,
        avg_weight=avg_weight,
        avg_steps=avg_steps,
        avg_water=avg_water
    )

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        conn = sqlite3.connect('health_tracker.db')
        c = conn.cursor()

        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
        except:
            conn.close()
            return "Username already exists"

        conn.close()
        return redirect('/login')

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('health_tracker.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect('/')
        else:
            return "Invalid username or password"

    return render_template('login.html')

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect('health_tracker.db')
    c = conn.cursor()
    c.execute("SELECT * FROM health_data WHERE user_id = ?", (session['user_id'],))
    data = c.fetchall()
    conn.close()

    return render_template('index.html', data=data)


@app.route('/add', methods=['GET', 'POST'])
def add():
    
    if request.method == 'POST':
        date = request.form['date']
        weight = request.form['weight']
        steps = request.form['steps']
        water = request.form['water']
        user_id = session.get('user_id')

        conn = sqlite3.connect('health_tracker.db')
        c = conn.cursor()
        c.execute("INSERT INTO health_data (date, weight, steps, water, user_id) VALUES (?, ?, ?, ?, ?)",
                  (date, weight, steps, water, user_id))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add_entry.html')



@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_entry(id):
    conn = sqlite3.connect('health_tracker.db')
    c = conn.cursor()

    if request.method == 'POST':
        date = request.form['date']
        weight = request.form['weight']
        steps = request.form['steps']
        water = request.form['water']

        c.execute("""
            UPDATE health_data
            SET date = ?, weight = ?, steps = ?, water = ?
            WHERE id = ?
        """, (date, weight, steps, water, id))

        conn.commit()
        conn.close()
        return redirect('/')

    # GET request → load existing data
    c.execute("SELECT * FROM health_data WHERE id = ?", (id,))
    entry = c.fetchone()
    conn.close()

    return render_template('edit_entry.html', entry=entry)


@app.route('/delete/<int:id>')
def delete_entry(id):
    conn = sqlite3.connect('health_tracker.db')
    c = conn.cursor()
    c.execute("DELETE FROM health_data WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# -------------------------
# RUN APP
# -------------------------
if __name__ == '__main__':
    init_db()
    init_user_db()
    app.run(debug=True)

=======
from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

# -------------------------
# DATABASE SETUP
# -------------------------

def init_user_db():
    conn = sqlite3.connect('health_tracker.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

def init_db():
    conn = sqlite3.connect('health_tracker.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS health_data (
                    id INTEGER PRIMARY KEY,
                    date TEXT,
                    weight REAL,
                    steps INTEGER,
                    water INTEGER,
                    user_id INTEGER
                )''')
    conn.commit()
    conn.close()

# -------------------------
# ROUTES
# -------------------------

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.context_processor
def inject_theme():
    theme = request.cookies.get("theme", "minimalist")
    return dict(theme=theme)

@app.route('/theme/<name>')
def switch_theme(name):
    allowed = ["minimalist", "tailwind", "bootstrap", "dark"]
    if name in allowed:
        resp = redirect(request.referrer or '/')
        resp.set_cookie("theme", name)
        return resp
    return "Invalid theme", 400

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('health_tracker.db')
    c = conn.cursor()

    c.execute("SELECT date, weight, steps, water FROM health_data ORDER BY date")
    rows = c.fetchall()
    conn.close()

    if not rows:
        return render_template(
            "dashboard.html",
            dates=[],
            weights=[],
            steps=[],
            water=[],
            total_entries=0,
            avg_weight=0,
            avg_steps=0,
            avg_water=0
        )

    dates = [row[0] for row in rows]
    weights = [row[1] for row in rows]
    steps = [row[2] for row in rows]
    water = [row[3] for row in rows]

    total_entries = len(rows)
    avg_weight = round(sum(weights) / total_entries, 1)
    avg_steps = int(sum(steps) / total_entries)
    avg_water = int(sum(water) / total_entries)

    return render_template(
        "dashboard.html",
        dates=dates,
        weights=weights,
        steps=steps,
        water=water,
        total_entries=total_entries,
        avg_weight=avg_weight,
        avg_steps=avg_steps,
        avg_water=avg_water
    )

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        conn = sqlite3.connect('health_tracker.db')
        c = conn.cursor()

        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
        except:
            conn.close()
            return "Username already exists"

        conn.close()
        return redirect('/login')

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('health_tracker.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect('/')
        else:
            return "Invalid username or password"

    return render_template('login.html')

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect('health_tracker.db')
    c = conn.cursor()
    c.execute("SELECT * FROM health_data WHERE user_id = ?", (session['user_id'],))
    data = c.fetchall()
    conn.close()

    return render_template('index.html', data=data)


@app.route('/add', methods=['GET', 'POST'])
def add():
    
    if request.method == 'POST':
        date = request.form['date']
        weight = request.form['weight']
        steps = request.form['steps']
        water = request.form['water']
        user_id = session.get('user_id')

        conn = sqlite3.connect('health_tracker.db')
        c = conn.cursor()
        c.execute("INSERT INTO health_data (date, weight, steps, water, user_id) VALUES (?, ?, ?, ?, ?)",
                  (date, weight, steps, water, user_id))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add_entry.html')



@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_entry(id):
    conn = sqlite3.connect('health_tracker.db')
    c = conn.cursor()

    if request.method == 'POST':
        date = request.form['date']
        weight = request.form['weight']
        steps = request.form['steps']
        water = request.form['water']

        c.execute("""
            UPDATE health_data
            SET date = ?, weight = ?, steps = ?, water = ?
            WHERE id = ?
        """, (date, weight, steps, water, id))

        conn.commit()
        conn.close()
        return redirect('/')

    # GET request → load existing data
    c.execute("SELECT * FROM health_data WHERE id = ?", (id,))
    entry = c.fetchone()
    conn.close()

    return render_template('edit_entry.html', entry=entry)


@app.route('/delete/<int:id>')
def delete_entry(id):
    conn = sqlite3.connect('health_tracker.db')
    c = conn.cursor()
    c.execute("DELETE FROM health_data WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# -------------------------
# RUN APP
# -------------------------
if __name__ == '__main__':
    init_db()
    init_user_db()
    app.run(debug=True)

>>>>>>> e7674ccabe04af7913a4d14d87f184666d3a9002
