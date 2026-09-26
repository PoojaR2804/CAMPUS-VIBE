
from flask import (
    Flask, render_template, request, jsonify,
    redirect, url_for, session, flash
)
from pymongo import MongoClient
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps


app = Flask(__name__, template_folder="../frontend/templates")

# Secret key for session management
app.secret_key = "campusvibe_secret_key_2026"

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")

# Database
db = client["college_event_db"]

# Collections
events_collection = db["events"]
registrations_collection = db["registrations"]
users_collection = db["users"]


# =========================
# LOGIN REQUIRED DECORATOR
# =========================
def login_required_api(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            return jsonify({
                "error": "Please login to continue.",
                "redirect": url_for("login")
            }), 401

        return f(*args, **kwargs)

    return decorated_function


# =========================
# WELCOME / LOGO PAGE
# =========================
@app.route("/")
def welcome():
    if session.get("user_id"):
        return redirect(url_for("home"))

    return render_template("welcome.html")


# =========================
# HOME PAGE - LOGIN REQUIRED
# =========================
@app.route("/home")
def home():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    return render_template("index.html")


# =========================
# TEST MONGODB CONNECTION
# =========================
@app.route("/test-db")
def test_db():
    try:
        client.admin.command("ping")
        return "MongoDB connected successfully!"
    except Exception as e:
        return f"MongoDB connection failed: {e}"


# =========================
# STUDENT SIGNUP
# =========================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        register_no = request.form.get("register_no", "").strip()
        department = request.form.get("department", "").strip()
        password = request.form.get("password", "")

        if not all([name, email, register_no, department, password]):
            flash("Please fill in all fields.", "danger")
            return redirect(url_for("signup"))

        if len(password) < 8:
            flash("Password must contain at least 8 characters.", "danger")
            return redirect(url_for("signup"))

        # Check if email already exists
        if users_collection.find_one({"email": email}):
            flash("Email already registered. Please login.", "warning")
            return redirect(url_for("signup"))

        # Check if registration number already exists
        if users_collection.find_one({"register_no": register_no}):
            flash("Registration number already exists.", "warning")
            return redirect(url_for("signup"))

        user = {
            "name": name,
            "email": email,
            "register_no": register_no,
            "department": department,
            "password": generate_password_hash(password)
        }

        users_collection.insert_one(user)

        flash("Account created successfully! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")


# =========================
# STUDENT LOGIN
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = users_collection.find_one({"email": email})

        if user and check_password_hash(user["password"], password):
            session.clear()
            session["user_id"] = str(user["_id"])
            session["user_name"] = user["name"]
            session["user_email"] = user["email"]

            flash("Login successful!", "success")
            return redirect(url_for("home"))

        flash("Invalid email or password.", "danger")
        return redirect(url_for("login"))

    return render_template("login.html")


# =========================
# STUDENT LOGOUT
# =========================
@app.route("/logout")
def logout():
    session.clear()
    flash("You have logged out successfully.", "success")
    return redirect(url_for("welcome"))


# =========================
# EVENT REGISTRATION
# LOGIN REQUIRED
# =========================
@app.route("/api/registrations", methods=["POST"])
@login_required_api
def add_registration():
    registration = request.get_json(silent=True)

    if not registration:
        return jsonify({
            "error": "No registration data received"
        }), 400

    user_id = session.get("user_id")

    try:
        # Find logged-in student
        user = users_collection.find_one({
            "_id": ObjectId(user_id)
        })

        if not user:
            session.clear()
            return jsonify({
                "error": "User not found. Please login again.",
                "redirect": url_for("login")
            }), 401

        # Get event details
        event_id = registration.get("eventId")
        event_name = registration.get("eventName")

        if not event_id or not event_name:
            return jsonify({
                "error": "Event information is missing."
            }), 400

        # Prepare registration using verified student details
        new_registration = {
            "user_id": user_id,
            "eventId": event_id,
            "eventName": event_name,
            "name": user["name"],
            "email": user["email"],
            "registerNo": user["register_no"],
            "department": user["department"],
            "registeredAt": registration.get("registeredAt")
        }

        result = registrations_collection.insert_one(new_registration)

        return jsonify({
            "message": "Registration successful",
            "id": str(result.inserted_id)
        }), 201

    except Exception:
        app.logger.exception("Registration error")
        return jsonify({
            "error": "Unable to complete registration."
        }), 500


# =========================
# GET LOGGED-IN STUDENT'S REGISTRATIONS
# =========================
@app.route("/api/registrations", methods=["GET"])
@login_required_api
def get_registrations():
    try:
        user_id = session.get("user_id")

        registrations = list(
            registrations_collection.find({
                "user_id": user_id
            })
        )

        for registration in registrations:
            registration["_id"] = str(registration["_id"])

        return jsonify(registrations), 200

    except Exception:
        app.logger.exception("Error loading registrations")
        return jsonify({
            "error": "Unable to load registrations."
        }), 500


# =========================
# CANCEL OWN REGISTRATION
# =========================
@app.route(
    "/api/registrations/<registration_id>",
    methods=["DELETE"]
)
@login_required_api
def delete_registration(registration_id):
    try:
        user_id = session.get("user_id")

        result = registrations_collection.delete_one({
            "_id": ObjectId(registration_id),
            "user_id": user_id
        })

        if result.deleted_count == 0:
            return jsonify({
                "error": "Registration not found or access denied."
            }), 404

        return jsonify({
            "message": "Registration cancelled successfully"
        }), 200

    except Exception:
        return jsonify({
            "error": "Invalid registration ID"
        }), 400


# =========================
# RUN APPLICATION
# =========================
if __name__ == "__main__":
    app.run(debug=True)