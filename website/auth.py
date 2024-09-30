from flask import Blueprint, request, render_template, redirect, flash, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import re

from sqlalchemy.exc import IntegrityError

from .helpers import *
from .models import User
from . import db
# from . import Session
auth = Blueprint('auth', __name__)

@auth.route("/login" , methods = ["GET","POST"])
def login():
    
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        
        if (not email or not password):
            flash('Both inputs are required. Please try again.', category='error')    
            return redirect(url_for('views.welcome_login'))
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash(f'Welcome {user.username}!', category='success')
                session['user_id'] = user.id
                return redirect(url_for('views.home'))
            else:
                flash('Wrong Password. Please try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    
    return redirect(url_for('views.welcome_login'))

@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('views.welcome_login'))

@auth.route("/register", methods=['GET', 'POST'])
def register():
    drivers, constructors = get_drivers_constructors()
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if request.method == 'POST':
        
        email= request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_pass = request.form.get('confirm')
        fav_team = request.form.get('team')
        fav_driver = request.form.get('driver')
        
        if (not email) or (not username) or (not password) or (not confirm_pass) or (not fav_team) or (not fav_driver):
            flash('All fields are required.' , category='error')
        elif password != confirm_pass:
            flash("Passwords do not match.", category='error')
        elif  re.match(email_regex, email) is None:
            flash("Please enter a valid email", category='error')
        else:
            try:
                user = User( email=email, username=username, password=generate_password_hash(password,method='scrypt'), fav_team = fav_team, fav_driver = fav_driver)
                db.session.add(user)
                db.session.commit()
                flash('Succesfully Registered', category='success')
                print(f"{email} {username} {password} {confirm_pass} {fav_team} {fav_driver}")
                return redirect(url_for('views.welcome_login'))
            
            except IntegrityError as e:
                db.session.rollback()
                flash('Username or Email already exist.', category='error')
                return render_template('register.html', drivers = drivers, constructors = constructors)
        
        return render_template('register.html', drivers = drivers, constructors = constructors)
    # GET   
    else:
        
        return render_template('register.html', drivers = drivers, constructors = constructors)

@auth.route("/forgot", methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_pass = request.form.get('confirm')
        
        print(email )
        if (not email) or (not password) or (not confirm_pass):
            flash('All fields are required.' , category='error')
        elif password != confirm_pass:
            flash("Passwords do not match.", category='error')
        
        else:
            user = db.session.execute(
                db.select(User).filter(User.email == email)
            ).scalar()
            
            if user is None:
                flash("Email does not exists", category='error')
            else:
                user.password = generate_password_hash(password, 'scrypt')
                db.session.commit()
        
            return redirect(url_for('views.welcome_login'))
    

    return render_template('forgot-password.html')