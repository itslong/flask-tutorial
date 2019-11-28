from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User


"""
A common pattern with decorators is to use them to register functions as callbacks for certain events. 
In this case, the @app.route decorator creates an association between the URL given as an argument and the function. 
In this example there are two decorators, which associate the URLs / and /index to this function. 
This means that when a web browser requests either of these two URLs, 
Flask is going to invoke this function and pass the return value of it back to the browser as a response.
"""

@app.route('/')
def test():
    user = {'username': 'Test'}
    return render_template('index.html', user=user)

@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': 'Clark Kent',
            'body': 'im superman'
        },
        {
            'author': 'Bruce Wayne',
            'body': 'where my bat signal at'
        },
        {
            'author': 'The Flash',
            'body': 'bruh, im fast'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        # there will be either one or zero results
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

        # if the "next" param is not in the query string, replace it with the index endpoint.
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You have now registered.')
        return redirect(url_for('login'))

    return render_template('registration.html', title='Register', form=form)
