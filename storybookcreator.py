"""Server for creating storybooks."""
from flask import Flask, render_template, request, flash, session, redirect

from model import connect_to_db, db
import crud
import cloudinary
import os
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


# require('dotevn').config();
# const cloudinary = require('cloudinary').v2;

@app.route('/')
def show_homepage():
    """View homepage"""
    return render_template('/login.html')


@app.route('/user_registration_route')
def route_to_registration_page():
    """take user to registration page"""
    return render_template("/user_registration.html")


@app.route('/user_registration', methods = ['POST'])
def user_reg_post_intake():
    email = request.form.get('email')
    password = request.form.get('password')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    session['fname'] = fname
    email_check = crud.get_user_by_email(email)

    if email_check:
        flash("A user already exists with that email.  Please try again")
        return redirect('/user_registration.html')
    else:
        create_user = crud.create_user(email, password, fname, lname)
        flash("Your account has successfully been registered. Please log in.")

        return render_template('/login.html', create_user=create_user)

@app.route('/login', methods = ['POST'])
def login():
    """Process login"""
    email = request.form.get('email')
    password= request.form.get('password')
    login = crud.check_login(email, password)
    
    if login:
        flash("You have successfully logged in.")
        return crud.get_users_fname(email)
    else:
        flash("This password didnt match the user login.")
        return redirect('/login.html')

@app.route('/library')
def go_to_user_libary_page():
    """take user to their library"""
    email = request.form.get('email')
    fname = crud.get_users_fname(email)
    return render_template('library.html', fname=fname)


@app.route('/pages')
def go_to_make_pages():
    """take user to create book pages"""
    
    return render_template('page.html')

@app.route('/page-creation', methods=["POST"])
def create_text_and_images_for_pages():
    """creating text and images for each page"""
    first_sentence = request.form.get("first-sentence")
    second_sentence = request.form.get("second-sentence")
    third_sentence = request.form.get("third-sentence")
    session['first_sentence'] = first_sentence
    session['second_sentence'] = second_sentence
    session['third_sentence'] = third_sentence
    page_text = f'{first_sentence}  {second_sentence}  {third_sentence}'
    page_image = request.form.get("image-upload")
    author = f'{fname} {lname}'
    book_id = crud.create_book(author, book_id)
    create_book_page = crud.create_book_page(page_number, page_text, page_image, book_id)


    return render_template("created-page.html", first_sentence=first_sentence,second_sentence=second_sentence,third_sentence=third_sentence, page_image=page_image)


if __name__ == '__main__':
    
    connect_to_db(app)
  
    app.run(host='0.0.0.0', debug=True)