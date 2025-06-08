from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from dotenv import load_dotenv
import os
import random
import time

app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")

# Twilio setup
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
client = Client(account_sid, auth_token)

# Database setup
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(15), nullable=False)

# Create database
with app.app_context():
    db.create_all()

# Generate 6-digit code
def generate_code():
    return str(random.randint(100000, 999999))

# Send OTP helper
def send_otp(user, code):
    try:
        client.messages.create(
            body=f"Your 2FA code is: {code}",
            from_=twilio_number,
            to=user.phone
        )
        return True
    except TwilioRestException as e:
        if e.code == 21608:
            flash("Your phone number is unverified. Please contact the admin to verify it.")
        else:
            flash(f"Failed to send OTP: {str(e)}")
        return False

@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        phone = request.form["phone"]
        if User.query.filter_by(username=username).first():
            flash("Username already exists!")
            return redirect(url_for("register"))
        user = User(username=username, password=password, phone=phone)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful! Please log in.")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if "pending_user_id" in session:
            flash("Verification already in progress. Check your phone!")
            return redirect(url_for("verify"))
        
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            code = generate_code()
            session["pending_user_id"] = user.id
            session["verification_code"] = code
            session["otp_sent_time"] = time.time()  # For logout timer
            print(f"Generated OTP for {username}: {code}")
            if send_otp(user, code):
                flash("Sending OTP... Please check your phone.")
                return redirect(url_for("verify"))
            session.pop("pending_user_id", None)
            session.pop("verification_code", None)
            session.pop("otp_sent_time", None)
            return redirect(url_for("login"))
        flash("Invalid credentials!")
    return render_template("login.html")

@app.route("/verify", methods=["GET", "POST"])
def verify():
    if "pending_user_id" not in session:
        flash("Please log in first!")
        return redirect(url_for("login"))
    if request.method == "POST":
        action = request.form.get("action")
        if action == "resend":
            user = User.query.get(session["pending_user_id"])
            code = generate_code()
            session["verification_code"] = code
            print(f"Resent OTP for {user.username}: {code}")
            if send_otp(user, code):
                flash("New OTP sent! Check your phone.")
            return redirect(url_for("verify"))
        code = request.form["code"]
        stored_code = session.get("verification_code")
        print(f"Entered OTP: {code}, Stored OTP: {stored_code}")
        if code == stored_code:
            session["user_id"] = session.pop("pending_user_id")
            session["login_time"] = time.time()  # For logout timer
            session.pop("verification_code")
            session.pop("otp_sent_time")
            return redirect(url_for("dashboard"))
        flash("Invalid code!")
    return render_template("verify.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    # Auto-logout after 10 minutes (600 seconds)
    if "login_time" in session and (time.time() - session["login_time"]) > 600:
        session.pop("user_id", None)
        session.pop("login_time", None)
        flash("Session expired. Please log in again.")
        return redirect(url_for("login"))
    
    user = User.query.get(session["user_id"])
    if request.method == "POST":
        new_password = request.form.get("password")
        new_phone = request.form.get("phone")
        if new_password:
            user.password = new_password
        if new_phone:
            user.phone = new_phone
        db.session.commit()
        flash("Profile updated successfully!")
        return redirect(url_for("dashboard"))
    
    return render_template("dashboard.html", user=user)

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("pending_user_id", None)
    session.pop("verification_code", None)
    session.pop("login_time", None)
    session.pop("otp_sent_time", None)
    flash("Logged out successfully!")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)