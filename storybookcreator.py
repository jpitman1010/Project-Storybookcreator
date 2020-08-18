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
    session['fname'] = fname
    session['email'] = email
    email_check = crud.get_user_by_email(email)

    if email_check:
        flash("A user already exists with that email.  Please try again")
        return redirect('/user_registration.html')
    else:
        create_user = crud.create_user(email, password, fname, lname)
        flash("Your account has successfully been registered. Please log in.")

        return render_template('/login.html', create_user=create_user,fname=fname,email=email, lname=lname)

@app.route('/login', methods = ['POST'])
def login():
    """Process login"""
    email = request.form.get('email')
    password = request.form.get('password')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    session['fname'] = fname
    session['email'] = email
    login = crud.check_login(email, password)
    
    if login:
        flash("You have successfully logged in.")
        return render_template("library.html", fname=fname, email=email)
    else:
        flash("This password didnt match the user login.")
        return redirect('/login.html')

@app.route('/library')
def go_to_user_libary_page():
    """take user to their library"""
    email = session['email']
    fname = crud.get_users_fname(email)
    author_id = crud.get_user_by_id(email)
    book_title_list = crud.get_book_id(email)
    session['book_title_list'] = book_id_list
    title = crud.create_book()[-1]
    completed_book = crud.get_completed_book(book_id,author_id, title)
    session['fname']=fname

    return render_template('library.html', fname=fname, email=email, book_title_list=book_title_list)


@app.route('/cover_page_creation', methods=["POST"])
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

    print('cloudinary response', [response])
    print("type", type(response)) 
    print('dir', dir(response))
    app.logger.info("uploaded:"+str(response))

    cover_image = response['url']
   
    session['cover_image'] = cover_image
    
    app.logger.info('cover_image:'+cover_image)
    title = request.form.get('title')
    page_text = f'{title}'
    email = session['email']
    book_id = crud.get_book_id()
    page_id = crud.get_page_id(book_id)
    create_book = crud.create_book(email)
    create_cover_page = crud.create_cover_page(page_text, cover_image, email)

    return render_template("cover_page_creation.html",title=title, cover_image=cover_image,create_cover_page=create_cover_page,create_book=create_book ) 


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
    print(file, type(file), dir(file))

    if file.filename == '':
        raise Exception('No selected file')

    response = cloudinary.uploader.upload(file)

    print('cloudinary response', [response])
    print("type", type(response)) 
    print('dir', dir(response))
    app.logger.info("uploaded:"+str(response))

    first_sentence = request.form.get("sentence1")
    second_sentence = request.form.get("sentence2")
    third_sentence = request.form.get("sentence3")
    
    session['first_sentence'] = first_sentence
    session['second_sentence'] = second_sentence
    session['third_sentence'] = third_sentence

    page_image = response['url']
    

    app.logger.info('page_image:'+page_image)
    page_text = f"""
    {first_sentence} 
    {second_sentence} 
    {third_sentence}"""

    email = session['email']
    session['page_image']=page_image
    book_id = crud.get_book_id()
    page_id = crud.get_page_id(book_id)

    create_book_page = crud.create_book_page(page_text, page_image, email)


    return render_template("created-page.html",first_sentence=first_sentence,second_sentence=second_sentence,third_sentence=third_sentence, page_image=page_image,create_book_page=create_book_page) 



@app.route('/save_and_complete_book', methods=['POST'])
def save_completed_book():
    """ends book creation and shows complete created book in library"""

    return render_template("library.html")



if __name__ == '__main__':
    
    connect_to_db(app)
  
    app.run(host='0.0.0.0', debug=True, use_reloader=True)