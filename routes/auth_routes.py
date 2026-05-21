from flask import Blueprint, render_template
from flask import request, redirect

from database.db import companies_collection

auth_bp = Blueprint("auth", __name__)


# ---------------- REGISTER PAGE ----------------

@auth_bp.route("/register", methods=["GET"])
def register_page():

    return render_template("register.html")


# ---------------- REGISTER COMPANY ----------------

@auth_bp.route("/register", methods=["POST"])
def register_company():

    data = request.form

    existing = companies_collection.find_one({
        "email": data["email"]
    })

    if existing:
        return "Company already exists"

    company = {
        "company_name": data["company_name"],
        "email": data["email"],
        "password": data["password"]
    }

    companies_collection.insert_one(company)

    return redirect("/login")


# ---------------- LOGIN PAGE ----------------

@auth_bp.route("/login", methods=["GET"])
def login_page():

    return render_template("login.html")


# ---------------- LOGIN ----------------

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.form

    company = companies_collection.find_one({
        "email": data["email"],
        "password": data["password"]
    })

    if company:
        return redirect("/dashboard")

    return "Invalid Credentials"