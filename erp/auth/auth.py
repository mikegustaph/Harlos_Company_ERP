import os
import shutil
from erp.models.harlos_db import db, Users
from erp.admin.admin import admin_bp
from flask_login import login_user, logout_user, login_required
from flask import Blueprint, render_template, request, url_for, redirect, flash

auth_bp = Blueprint(
    "auth_bp",
    __name__,
    url_prefix="/",
    template_folder="templates",
    static_folder="static",
    static_url_path="assets",
)


@auth_bp.route("/signin", methods=["POST", "GET"])
def signin():
    if request.method == "POST":
        useremail = request.form.get("email")
        password = request.form.get("password")
        remember_me = request.form.get("remember_me")
        if all([useremail, password]):
            user_exists = Users.query.filter_by(email=useremail).first()
            if user_exists:
                if user_exists.is_authorised(password) and user_exists.is_active:
                    login_user(user_exists)
                    return redirect(url_for("home_bp.index"))
                flash("Invalid Password/Username ")
                return render_template("signin.html")
            flash("User with this email cannot be found")
            return render_template("signin.html")
    return render_template("signin.html", title="Sign In")


@auth_bp.route("/signout", methods=["GET"])
def signout():
    print("logging out the user")
    logout_user()
    return redirect(url_for("auth_bp.signin"))
