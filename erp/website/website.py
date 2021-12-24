import flask_login
from flask_login import login_required
from flask import Blueprint, url_for, redirect, render_template, request
from erp.models.harlos_db import db, Testimonials, customerStatistics


website_bp = Blueprint(
    "website_bp",
    __name__,
    url_prefix="/",
    template_folder="templates",
    static_folder="static",
    static_url_path="assets",
)


def add_new_testimonial(testmonial_data: dict) -> bool:
    name = testmonial_data.get("t_name")
    title = testmonial_data.get("t_title")
    review = testmonial_data.get("review")

    if all([name, title, review]):
        new_testimonial = Testimonials(name=name, title=title, review=review)

        try:
            db.session.add(new_testimonial)
            db.session.commit()
            print("testimony done")
            return True
        except Exception as bug:
            print(bug)
            return False
    print([name, title, review])
    return False


def load_all_testimonials(as_json=False):
    try:
        all_testimonials = Testimonials.query.all()
        if not as_json:
            return all_testimonials if all_testimonials else []
        all_testimonials = [
            {
                "name": testimony.name,
                "title": testimony.title,
                "review": testimony.review,
            }
            for testimony in all_testimonials
        ]
        return all_testimonials
    except Exception as bug:
        print(bug)
        return []


def add_custom_statistics(customer_statistics: dict) -> bool:
    try:
        countries = customer_statistics.get("countries")
        customers = customer_statistics.get("customers")
        ports = customer_statistics.get("ports")
        if all([customers, ports, countries]):
            stat_exist = customerStatistics.query.filter_by(id=1).first()
            if stat_exist:
                if countries:
                    stat_exist.countries = countries
                if customers:
                    stat_exist.customers = customers
                if ports:
                    stat_exist.ports = ports
                db.session.add(stat_exist)
            else:
                new_stat = customerStatistics(
                    countries=countries, customers=customers, ports=ports
                )
                db.session.add(new_stat)
            db.session.commit()
            return True
        return False

    except Exception as bug:
        print(bug)
        return False


def load_customer_statistics(as_json=False):
    try:
        stats = customerStatistics.query.filter_by(id=1).first()
        if not as_json:
            return stats if stats else []

        return {
            "customers": stats.customers,
            "countries": stats.countries,
            "ports": stats.ports,
        }
    except Exception as bug:
        print(bug)
        return {}


@website_bp.route("/ecommerce-config", methods=["GET", "POST"])
@login_required
def website():
    if flask_login.current_user.is_admin:
        if request.method == "POST":
            add_new_testimonial(request.form)
        return render_template(
            "website-config.html",
            title="Ecommerce Configurations",
            all_testmonials=load_all_testimonials(),
        )
    return redirect(url_for("home_bp._401"))


@website_bp.route("/ecommerce-stats", methods=["GET", "POST"])
@login_required
def stats():
    if flask_login.current_user.is_admin:
        if request.method == "POST":
            add_custom_statistics(request.form)
        return render_template(
            "website-stats.html",
            title="Ecommerce Statistics",
            customer_stats=load_customer_statistics(),
        )
    return redirect(url_for("home_bp._401"))


@website_bp.route("delete-testimony/<int:testimony_id>")
def delete_testimony(testimony_id: int):
    if flask_login.current_user.is_admin:
        try:
            testimony_id = int(testimony_id)
            target_testimony = Testimonials.query.filter_by(id=testimony_id).first()
            if target_testimony:
                db.session.delete(target_testimony)
                db.session.commit()
            return redirect(url_for("website_bp.website"))
        except Exception as bug:
            print(bug)
            return redirect(url_for("website_bp.website"))
    return redirect(url_for("home_bp.401"))
