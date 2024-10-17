from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user


gen = Blueprint('gen', __name__)



@gen.route('/', methods=['GET'])
@login_required
def home():
    response_data=1
    return render_template("base.html", user=current_user)


