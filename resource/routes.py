# Imports
import os
from flask import Blueprint, redirect, url_for, render_template, request, abort
from flask import current_app as cur_app, flash
from flask_login import current_user as cur_usr, login_required as log_req
from flask_login import login_user, logout_user
from .models import User
from .extensions import db
from werkzeug.utils import secure_filename

# Blueprint
main = Blueprint("main", __name__)

# Routes
# Landing Page, it should redirect to dashboard if the user is logged in
@main.route("/")
def landing():
    # if cur_usr.is_authenticated:
    #     return redirect(url_for("main.dashboard"))
    return render_template("landing.html")

# Dashboard page
@main.route("/dashboard")
@log_req
def dashboard():
    # Connect skills to the User_Skill Database, which will in-turn
    # be connected to a Universal Skill Database
    skills = [
        {'name' : 'Python', 'percent' : 80},
        {'name' : 'SQL (Basics)', 'percent' : 75},
        {'name' : 'Excel', 'percent' : 60}
    ]

    # Connect jobs to the User_job_match Database, which will in-turn
    # be connected to a Universal jobs Database
    jobs = [
        {
            "title":"Data Analyst", 
            "location":"Mumbai", 
            "package":"8-9 LPA"},
        {
            "title":"Business Analyst", 
            "location":"Pune", 
            "package":"6 - 7 LPA"},
        {
            "title":"Marketing Associate", 
            "location":"Delhi", 
            "package":"To Be Discussed"},
        {
            "title":"Junior Developer", 
            "location":"Rohtak", 
            "package":"5 LPA"},
        {
            "title":"Full-Stack Developer", 
            "location":"Haryana", 
            "package":"8 LPA"
         }
        
    ]

    return render_template(
        "dashboard.html",
        skills = skills,
        jobs = jobs,
        profile_score = 72, # Implement the user_analysis
        jobs_matched = 32 # Implement the user_analysis
    )

# Register Pop-Up Form
@main.route("/register", methods=["POST"])
def register():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    # Check for the existence of email in User DataBase
    # if present redirect to landing page.
    if User.query.filter_by(u_email=email).first():
        flash("Email already registered.")
        return redirect(url_for("main.landing"))
    
    # Create the user if email not present in DB, set password
    # Add the user to database -> commit changes
    user = User(u_name=name, u_email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    # Log the user in, disabled(redirect to dashbord) redirets to landing page now.
    login_user(user=user)
    return redirect(url_for("main.landing"))

# Login Pop-up Form
@main.route("/signin", methods=["POST"])
def signin():
    # Get the email and password from the form
    email = request.form["email"]
    password = request.form["password"]

    # Select the user if present in DB, print a message otherwise
    user = User.query.filter_by(u_email=email).first()

    # if user ad password match login and disabled(go to dashboard)  redirets to landing page now,
    # # else -> landing
    if user and user.check_password(password):
        login_user(user=user)
        return redirect(url_for("main.landing"))
    flash("Invalid Credentials.")
    return redirect(url_for("main.landing"))

# Log Out
@main.route("/logout")
@log_req
def logout():
    logout_user()
    return redirect(url_for("main.landing"))

# admin Page
@main.route("/admin")
@log_req
def admin():
    # Check for the admin priviledges:
    if not cur_usr.is_admin():
        abort(403)
    
    # If admin give access to DB
    users = User.query.all()
    return render_template("admin.html", users=users)

#File-Upload route
ALLOWED_TYPES = {'pdf', 'docx'}
def allowed_file(filename):
    if "." not in filename:
        return False

    extension = filename.split(".")[-1].lower()
    return extension in ALLOWED_TYPES

@main.route("/upload_resume", methods=['POST'])
@log_req
def upload_resume():
    if 'resume' not in request.files:
        return redirect(url_for("main.dashboard"))
    
    resume_file = request.files['resume']

    if resume_file.filename == "":
        return redirect(url_for("main.dashboard"))
    if resume_file and allowed_file(resume_file.filename):
        resume_filename = secure_filename(resume_file.filename)
        uniq_resume_filename = f"user_{cur_usr.u_id}_{resume_filename}"
        resume_filepath = os.path.join(cur_app.config['UPLOAD_FOLDER'], uniq_resume_filename)

        resume_file.save(resume_filepath)

        cur_usr.u_resume_path = uniq_resume_filename
        db.session.commit()

        flash("Resume uploaded successfully!")
        return redirect(url_for("main.dashboard"))
    return redirect(url_for("main.dashboard"))

# profile route
@main.route("/profile")
@log_req
def profile():
    return render_template('profile.html')

# result route
@main.route("/result")
@log_req
def result():
    return render_template('result.html')

# roadmap route
@main.route("/roadmap")
@log_req
def roadmap():
    return render_template('roadmap.html')

# roadmap route
@main.route("/jobs")
@log_req
def jobs():
    return render_template('jobs.html')
