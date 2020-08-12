
"""Server for creating storybooks."""
from flask import (Flask, render_template, request, flash, session,
                   redirect)

from jinja2 import StrictUndefined
from model import connect_to_db
import crud


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def show_homepage():
    """View homepage"""
    return render_template('/login.html')


@app.route('/user_registration', methods = ['POST'])
def user_reg_post_intake():
    email = request.form.get('email')
    password = request.form.get('password')
    fname = request.form.get('fname')
    lname = request.form.get('lname')


    email_check = crud.get_user_by_email(email)

    if email_check:
        flash("A user already exists with that email.  Please try again")
    else:
        create_user = crud.create_user(email, password, fname, lname,user_id)
        flash(f"""Your account was created successfully. 
        Your user ID is {user_id} You will now be logged in.  
        Be sure to write down your user ID = {user}
        and your secret password somewhere safe so that 
        you can log in each time. """)
    return redirect('/library.html')

@app.route('/login', methods = ['POST'])
def login():
    """Process login"""
    email = request.form.get('email')
    password= request.form.get('password')
    login = crud.check_login(email, password)

    if login:
        flash("You have successfully logged in.")
        # session['user_id'] = user_id
        return redirect('/library.html')
    else:
        flash("This password didnt match the user login.")
        return redirect('/login.html')



if __name__ == '__main__':
    
    connect_to_db(app)
  
    app.run(host='0.0.0.0', debug=True)
