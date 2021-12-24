import flask_login
from flask_login import login_required
from flask import Blueprint, url_for, redirect, render_template, request


profile_bp = Blueprint(
    "profile_bp",
    __name__,
    url_prefix="/",
    template_folder="templates",
    static_folder="static",
    static_url_path="assets",
)


@profile_bp.route("/profile")
@login_required
def profile():
    if flask_login.current_user.is_admin:
        return render_template("profile.html", title="Profile")
    return redirect(url_for("home_bp._401"))
