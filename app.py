from flask import Flask, render_template, request, redirect, flash, session
import mysql.connector
from mysql.connector import Error
from functools import wraps

app = Flask(__name__)
app.secret_key = "super_secret_key"

# ── Admin credentials ────────────────────────────────────────
import bcrypt

ADMIN_USERNAME = "darshan"

ADMIN_PASSWORD_HASH = "$2b$12$vo7233OTgNqtBp1sQ1huyuokHtmUX1qfRybqYKWuMykTOdO3WM/g6"

# ── Database config ──────────────────────────────────────────
db_config = {
    'host':     '127.0.0.1',
    'user':     'root',
    'password': '',
    'database': 'custermer_details'
}
# ── Login required decorator ───────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in'):
            flash("Please login to access the inbox.", "error")
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated

# ── Home Page ──────────────────────────────────────────────────
@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

# ── About Page ─────────────────────────────────────────────────
@app.route('/about.html')
def about():
    return render_template('about.html')

# ── Contact Page & Form Handling ───────────────────────────────
@app.route('/contact.html', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        full_name = request.form.get('name')
        email     = request.form.get('email')
        subject   = request.form.get('subject')
        message   = request.form.get('message')

        try:
            connection = mysql.connector.connect(**db_config)
            if connection.is_connected():
                cursor = connection.cursor()
                sql_insert_query = """
                    INSERT INTO Details (Full_name, Email, Subject, Message)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql_insert_query, (full_name, email, subject, message))
                connection.commit()
                flash("Your message has been sent successfully!", "success")
                return redirect('/contact.html')

        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            flash("An error occurred while sending your message. Please try again.", "error")

        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

    return render_template('contact.html')

# ── Login Page ─────────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if (
            username == ADMIN_USERNAME
            and bcrypt.checkpw(
                password.encode('utf-8'),
                ADMIN_PASSWORD_HASH.encode('utf-8')
            )
        ):
            session['logged_in'] = True
            session.permanent = False
            return redirect('/details.html')

        flash("Invalid username or password.", "error")

    return render_template('login.html')
# ── Logout ─────────────────────────────────────────────────────
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect('/login')

# ── Details Page (Protected) ───────────────────────────────────
@app.route('/details.html')
@login_required
def details():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        
        # Use SELECT * to avoid column name issues
        cursor.execute("SELECT * FROM Details")
        
        raw = cursor.fetchall()
        cursor.close()
        connection.close()

        # Print to terminal so you can see exact column names
        if raw:
            print("COLUMN NAMES:", list(raw[0].keys()))
            print("FIRST ROW:", raw[0])

        # Manually remap whatever columns come back
        messages = []
        for row in raw:
            messages.append({
                'id':         row.get('Sl.NO') or row.get('id') or row.get('ID') or 0,
                'Full_name':  row.get('Full_name') or row.get('full_name') or '',
                'Email':      row.get('Email') or row.get('email') or '',
                'Subject':    row.get('Subject') or row.get('subject') or '',
                'Message':    row.get('Message') or row.get('message') or '',
                'created_at': row.get('Date') or row.get('date') or row.get('created_at') or '',
            })

        return render_template('details.html', messages=messages)

    except Error as e:
        print(f"Database error: {e}")          # ← check your terminal for exact error
        flash("Could not load messages. Please try again.", "error")
        return redirect('/login')
if __name__ == '__main__':
    app.run(debug=True)