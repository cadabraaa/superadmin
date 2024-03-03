from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth= Blueprint('auth', __name__)




@auth.route('/sign_up', methods=['GET', 'POST'] )
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

    if user:
        flash('Email already exists.', category='error')
    elif len(email) < 4:
        flash('Email must be greater than 3 characters.', category='error')
    elif password1 != password2:
        flash('Passwords don\'t match.', category='error')
    elif len(password1) < 7:
        flash('Password must be at least 7 characters.', category='error')
    else:
        new_user = User(email=email, company_code=company_code, company_name=company_name, mobile=mobile, password=generate_password_hash(
            password1, method='pbkdf2:sha256'))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        flash('Account created!', category='success')
        return redirect(url_for('views.home'))

  return render_template("sign_up.html", user=current_user)

