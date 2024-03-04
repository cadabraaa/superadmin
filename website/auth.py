from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import re

auth = Blueprint('auth', __name__)


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
  if request.method == 'POST':
    company_code = request.form.get('company_code')
    company_name = request.form.get('company_name')
    establishment_year = request.form.get('establishment_year')
    mobile = request.form.get('mobile')
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    user = User.query.filter_by(email=email).first()
    c_code = User.query.filter_by(company_code=company_code).first()

    if user:
      flash('Email already exists.', category='error')
    elif c_code:
        flash('The company code already exists.', category='error')
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
      flash('Email is not valid.', category='error')
    else:
      new_user = User(email=email,
                      company_code=company_code,
                      company_name=company_name,
                      mobile=mobile,
                      establishment_year=establishment_year,
                      password=generate_password_hash(password1,
                                                      method='pbkdf2:sha256'))
      db.session.add(new_user)
      db.session.commit()
      login_user(new_user, remember=True)
      flash('Account created!', category='success')
      return redirect(url_for('views.home'))

  return render_template("sign_up.html", user=current_user)
