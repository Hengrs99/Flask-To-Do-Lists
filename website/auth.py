from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import models, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


# AUTHENTICATION


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    displays user login page
    :exception: POST
    :return: None
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = models.User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.user_lists'))
            else:
                flash('Incorrect password!', category='error')
        else:
            flash('This user does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    """
    logs user out and redirect to login page
    :return: None
    """
    logout_user()
    return redirect(url_for('views.about'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    """
    displays user sign up page
    :exception: POST
    :return: None
    """
    if request.method == 'POST':
        email = request.form.get('email')
        nickname = request.form.get('nickname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = models.User.query.filter_by(email=email).first()
        if user:
            flash('User alredy registered!', category='error')
        elif len(email) < 5:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(nickname) < 2:
            flash('Nickname must be greater than 1 characters.', category='error')
        elif password1 != password2:
            flash('Password don\'t match.', category='error')
        elif len(password1) < 8:
            flash('Password must be at least 7 characters long.', category='error')
        else:
            new_user = models.User(email=email, nickname=nickname,
                                   password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("Sign-up was successful! You are now signed in.", category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.user_lists'))

    return render_template("sign-up.html", user=current_user)
