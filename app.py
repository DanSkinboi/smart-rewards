import os
import sqlite3
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "smart_rewards.db")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SMART_REWARDS_SECRET", "change-this-before-deployment")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = os.environ.get("COOKIE_SECURE", "0") == "1"

def db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(_error):
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                phone TEXT NOT NULL UNIQUE,
                country TEXT NOT NULL,
                email TEXT,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

def login_required(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        if not session.get("member_id"):
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapped

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("full_name", "").strip()
        phone = request.form.get("phone", "").strip()
        country = request.form.get("country", "").strip()
        email = request.form.get("email", "").strip() or None
        password = request.form.get("password", "")
        if not name or not phone or country not in ("Nigeria", "Cameroon") or len(password) < 10:
            flash("Complete all required fields. Password must be at least 10 characters.")
            return render_template("register.html")
        try:
            cur = db().execute(
                "INSERT INTO members(full_name, phone, country, email, password_hash) VALUES (?, ?, ?, ?, ?)",
                (name, phone, country, email, generate_password_hash(password))
            )
            db().commit()
        except sqlite3.IntegrityError:
            flash("That phone number already has an account. Please log in.")
            return render_template("register.html")
        session.clear()
        session["member_id"] = cur.lastrowid
        return redirect(url_for("dashboard"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")
        member = db().execute("SELECT * FROM members WHERE phone = ?", (phone,)).fetchone()
        if member and check_password_hash(member["password_hash"], password):
            session.clear()
            session["member_id"] = member["id"]
            return redirect(url_for("dashboard"))
        flash("Login details were not recognised.")
    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    member = db().execute(
        "SELECT full_name, phone, country, created_at FROM members WHERE id = ?",
        (session["member_id"],)
    ).fetchone()
    if member is None:
        session.clear()
        return redirect(url_for("login"))
    return render_template("dashboard.html", member=member)

@app.route("/logout", methods=["POST"])
@login_required
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=False)
