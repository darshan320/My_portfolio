from flask import Flask, render_template, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='static')
app.secret_key = os.environ.get("SECRET_KEY", "super_secret_key")

# ── Database config ──────────────────────────────────────────
database_url = os.environ.get('DATABASE_URL', 'sqlite:///local.db')
if database_url.startswith('postgresql://'):
    database_url = database_url.replace('postgresql://', 'postgresql+psycopg://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ── Admin credentials ────────────────────────────────────────
ADMIN_USERNAME = "darshan"
ADMIN_PASSWORD_HASH = "$2b$12$vo7233OTgNqtBp1sQ1huyuokHtmUX1qfRybqYKWuMykTOdO3WM/g6"

# ── Model ────────────────────────────────────────────────────
class Detail(db.Model):
    __tablename__ = 'details'
    id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name  = db.Column(db.String(200))
    email      = db.Column(db.String(200))
    subject    = db.Column(db.String(300))
    message    = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

# ── Auto create tables ───────────────────────────────────────
with app.app_context():
    db.create_all()

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
                full_name=full_name,
                email=email,
                subject=subject,
                message=message
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
        rows = Detail.query.order_by(Detail.created_at.desc()).all()
        messages = [
            {
                'id':         r.id,
                'Full_name':  r.full_name  or '',
                'Email':      r.email      or '',
                'Subject':    r.subject    or '',
                'Message':    r.message    or '',
                'created_at': str(r.created_at) if r.created_at else '',
            }
            for r in rows
        ]
        return render_template('details.html', messages=messages)
    except Exception as e:
        print(f"Database error: {e}")
        flash("Could not load messages.", "error")
        return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)