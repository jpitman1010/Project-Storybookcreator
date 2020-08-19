"""Server for creating storybooks."""
from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db, Book,User,Page
import crud
import os
import sys
from jinja2 import StrictUndefined
import cloudinary
import cloudinary.uploader


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

cloud_name = os.environ['CLOUDINARY_CLOUD_NAME']  
cloud_api =os.environ['CLOUDINARY_API_KEY'] 
cloud_api_secret = os.environ['CLOUDINARY_API_SECRET'] 

cloudinary.config(
  cloud_name = cloud_name,  
  api_key = cloud_api,  
  api_secret = cloud_api_secret
)

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
    """take user registration info and make cookies"""
    email = request.form.get('email')
    password = request.form.get('password')
    fname = request.form.get('fname')
    lname = request.form.get('lname')

    print(email)
    email_check = crud.get_user_by_email(email)

    if email_check:
        flash("A user already exists with that email.  Please try again")
        print("Already a user")
        return redirect('/user_registration_route')
    else:
        create_user = crud.create_user(email, password, fname, lname)
        flash("Your account has successfully been registered. Please log in.")
        return render_template('/login.html', create_user=create_user,fname=fname,email=email, lname=lname)


@app.route('/login_form', methods=['POST'])
def login_form():
    """Process login and check for user in database"""

    password = request.form.get('password')
    email = request.form.get('email')

    fname = crud.get_users_fname(email)

    session['fname'] = fname
    session['email'] = email

    email_check = crud.get_user_by_email(email)
    password_check = crud.password_check(email, password)

    if  email_check:
        if  password_check:
            flash("You have successfully logged in.")
            print("You have successfully logged in.")
            return render_template("/library.html", fname=fname, email=email)
        else:
            flash("This password didnt match the user login.")
            print("This password didnt match the user login.")
            return redirect('/')
    else:
        flash("Sorry that is not a valid login email.  Please try again, or register as a new user.")
        print("Sorry that is not a valid login email.  Please try again, or register as a new user.")
        return redirect('/')


@app.route('/library')
def go_to_user_libary_page():
    """take user to their library"""

    email = session['email']
    fname = session['fname']

    return render_template("/library.html", fname=fname, email=email)



@app.route('/cover_page_creation')
def cover_page_route():
    """routes to page to creating text and images for cover page/storybook cover"""
    return render_template("/cover_page_creation.html")

@app.route('/cover_page_creation_form', methods=["POST"])
def create_text_and_images_for_cover_page():
    """creating text and images for cover page/storybook cover"""
    
    # check if the post request has the file part
    if 'image-upload' not in request.files:
        raise Exception('No file part')
    file = request.files['image-upload']
    print(file, type(file), dir(file))
    # if user does not select file, browser will also
    # submit an empty part without filename
    if file.filename == '':
        raise Exception('No selected file')
    response = cloudinary.uploader.upload(file)

    cover_image = response['url']
   
    title = request.form.get('title')
    email = session['email']
    page_text = f'{title}'
    create_book = crud.create_book(email, title)
    create_cover_page = crud.create_cover_page(page_text, cover_image, email)

    session['cover_image'] = cover_image
    session['title'] = title.title()

    

    return render_template("/page.html",title=title, cover_image=cover_image,create_cover_page=create_cover_page,create_book=create_book ) 

# @app.route('/created_cover_page')
# def add_cover_page_to_library():
#     """adds created coverpage to library as a thumbnail link to book"""

#     return render_template("/", cover_image=cover_image, title=title)

@app.route('/pages')
def go_to_make_pages():
    """take user to create book pages"""
    
    return render_template('page.html')


@app.route('/page-creation', methods=["POST"])
def create_text_and_images_for_pages():
    """creating text and images for each page"""
    
    # check if the post request has the file part
    if 'image-upload' not in request.files:
        raise Exception('No file part')
        # return redirect(request.url)
    file = request.files['image-upload']
    # print(file, type(file), dir(file))

    if file.filename == '':
        raise Exception('No selected file')

    response = cloudinary.uploader.upload(file)

    first_sentence = request.form.get("sentence1")
    second_sentence = request.form.get("sentence2")
    third_sentence = request.form.get("sentence3")
    
    session['first_sentence'] = first_sentence
    session['second_sentence'] = second_sentence
    session['third_sentence'] = third_sentence

    page_image = response['url']
    
    page_text = f"""
    {first_sentence} 
    {second_sentence} 
    {third_sentence}"""

    email = session['email']
    session['page_image'] = page_image
    session['page_text'] = page_text

    book_id = crud.get_book_id(email)
    page_id = crud.get_page_id(book_id)

    create_book_page = crud.create_book_page(page_text, page_image, email)


    return render_template("created-page.html",first_sentence=first_sentence,second_sentence=second_sentence,third_sentence=third_sentence, page_image=page_image,create_book_page=create_book_page) 



@app.route('/save_and_complete_book')
def save_completed_book():
    """ends book creation and shows complete created book in library"""
    
    email = session['email']
    book_id = crud.get_book_id(email)
    title = crud.get_book_title_list(email)[-1]

    session['book_id'] = book_id
    session['title'] = title

    return render_template("updated-library.html")



if __name__ == '__main__':
    
    connect_to_db(app)
  
    app.run(host='0.0.0.0', debug=True, use_reloader=True)