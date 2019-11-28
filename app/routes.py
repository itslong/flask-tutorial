from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user

from app import app
from app.forms import LoginForm
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
def index():
    data = [
        {
            'user': 'Clark Kent',
            'body': 'im superman'
        },
        {
            'user': 'Bruce Wayne',
            'body': 'where my bat signal at'
        },
        {
            'user': 'The Flash',
            'body': 'bruh, im fast'
        }
    ]
    return render_template('index.html', title='Home', data=data)

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
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
