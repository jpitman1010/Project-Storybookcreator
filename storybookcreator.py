
"""Server for creating storybooks."""
from flask import Flask, render_template, request, flash, session, redirect, jsonify
# from jinja2 import StringictUndefined
from model import connect_to_db, db, Page,Book,User
import model
import crud
import seed_database
import os
import cloudinary
import cloudinary.uploader 
import cloudinary.api

# result = cloudinary.uploader.unsigned_upload(file, upload_preset, **options)


app = Flask(__name__)
app.secret_key = "dev"
# app.jinja_env.undefined = StringictUndefined



cloudinary.config(
    cloud_name = 'cloud_name',
    api_key = 'cloudinary_api_key',
    api_secret = 'cloudinary_api_secret'
)


@app.route('/')
def show_homepage():
    """View homepage"""
    return render_template('/login.html')


@app.route('/user_regiStringation', methods = ['POST'])
def user_reg_post_intake():

    email = request.form.get('email')
    password = request.form.get('password')
    fname = request.form.get('fname')
    lname = request.form.get('lname')


    email_check = crud.get_user_by_email(email)

    if email_check:
        flash("A user already exists with that email.  Please try again")
        return redirect('/user_regiStringation.html')
    else:
        crud.create_user(email, password, fname, lname)
        return render_template('/library.html')

@app.route('/login', methods = ['POST'])
def login():
    """Process login"""
    email = request.form.get('email')
    password= request.form.get('password')
    login = crud.check_login(email, password)

    if login:
        flash("You have successfully logged in.")
        # session['user_id'] = user_id
        return render_template('/library.html')
    else:
        flash("This password didnt match the user login.")
        return redirect('/login.html')



@app.route('/page_image')
def add_image_to_page():
    """adding an image to a book page"""
    filename = request.files.get('image-upload')
    print(filename)
    if filename:
        response = cloudinary.uploader.upload(filename)
        print(response)
        image = response['secure_url']
        print(image)
        return render_template('pages.html')





if __name__ == '__main__':
    
    connect_to_db(app)
  
    app.run(host='0.0.0.0', debug=True)
