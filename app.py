from flask import Flask, render_template, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import bcrypt
import os

app = Flask(__name__, static_folder='static')
app.secret_key = os.environ.get("SECRET_KEY", "super_secret_key")

# ── Database config ──────────────────────────────────────────
MYSQL_HOST     = os.environ.get('MYSQL_HOST', '127.0.0.1')
MYSQL_PORT     = os.environ.get('MYSQL_PORT', '3306')
MYSQL_USER     = os.environ.get('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'custermer_details')

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ── Admin credentials ────────────────────────────────────────
ADMIN_USERNAME = "darshan"
ADMIN_PASSWORD_HASH = "$2b$12$vo7233OTgNqtBp1sQ1huyuokHtmUX1qfRybqYKWuMykTOdO3WM/g6"

# ── Model ────────────────────────────────────────────────────
class Detail(db.Model):
    __tablename__ = 'Details'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    Full_name  = db.Column('Full_name', db.String(200))
    Email      = db.Column('Email',     db.String(200))
    Subject    = db.Column('Subject',   db.String(300))
    Message    = db.Column('Message',   db.Text)
    created_at = db.Column('Date',      db.String(100))

# ── Login required decorator ─────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in'):
            flash("Please login to access the inbox.", "error")
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated

# ── Home ─────────────────────────────────────────────────────
@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

# ── About ────────────────────────────────────────────────────
@app.route('/about.html')
def about():
    return render_template('about.html')

# ── Work ─────────────────────────────────────────────────────
@app.route('/work.html')
def work():
    return render_template('work.html')

# ── Contact ──────────────────────────────────────────────────
@app.route('/contact.html', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        full_name = request.form.get('name')
        email     = request.form.get('email')
        subject   = request.form.get('subject')
        message   = request.form.get('message')
        try:
            new_msg = Detail(
                Full_name=full_name,
                Email=email,
                Subject=subject,
                Message=message
            )
            db.session.add(new_msg)
            db.session.commit()
            flash("Your message has been sent successfully!", "success")
            return redirect('/contact.html')
        except Exception as e:
            print(f"DB Error: {e}")
            flash("An error occurred. Please try again.", "error")
    return render_template('contact.html')

# ── Login ────────────────────────────────────────────────────
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

# ── Logout ───────────────────────────────────────────────────
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect('/login')

# ── Details (Protected) ──────────────────────────────────────
@app.route('/details.html')
@login_required
def details():
    try:
        messages = Detail.query.all()
        return render_template('details.html', messages=messages)
    except Exception as e:
        print(f"Database error: {e}")
        flash("Could not load messages.", "error")
        return redirect('/login')

# ── Test DB (remove after testing) ───────────────────────────
@app.route('/test-db')
def test_db():
    return (f"HOST: {MYSQL_HOST} | PORT: {MYSQL_PORT} | "
            f"USER: {MYSQL_USER} | DB: {MYSQL_DATABASE}")

if __name__ == '__main__':
    app.run(debug=True)