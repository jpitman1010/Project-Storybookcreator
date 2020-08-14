
"""Server for creating storybooks."""
from flask import Flask, render_template, request, flash, session, redirect

from jinja2 import StrictUndefined
from model import connect_to_db, db
import crud
# from cloudinary import requests, cloudinary.uploader, cloudinary.api
import os


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def show_homepage():
    """View homepage"""
    return render_template('/index.html')


@app.route('/', methods = ['POST'])
def user_reg_post_intake():
    email = request.form.get('email')
    password = request.form.get('password')
    fname = request.form.get('fname')
    lname = request.form.get('lname')


    email_check = crud.get_user_by_email(email)

    if email_check:
        flash("A user already exists with that email.  Please try again")
        return redirect('/index.html')
    else:
        create_user = crud.create_user(email, password, fname, lname)
        user_id = crud.get_user_by_id()
        flash(f"""Your account was created successfully. 
        Your user ID is {user_id} You will now be logged in.  
        Be sure to write down your user ID = {user_id}
        and your secret password somewhere safe so that 
        you can log in each time. """)
        return redirect('/index.html')

@app.route('/', methods = ['POST'])
def login():
    """Process login"""
    email = request.form.get('email')
    password= request.form.get('password')
    login = crud.check_login(email, password)

    if login:
        flash("You have successfully logged in.")
        # session['user_id'] = user_id
        return redirect('/index.html')
    else:
        flash("This password didnt match the user login.")
        return redirect('/index.html')


@app.route('/api/pageText')
def get_page_text():
    """get page-text from user-input in the text box"""
    return jsonify(pageText)




if __name__ == '__main__':
    
    connect_to_db(app)
  
    app.run(host='0.0.0.0', debug=True)
