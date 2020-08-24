"""Script to seed database."""

from flask_sqlalchemy import SQLAlchemy

import os
import json
from random import choice, randint
from datetime import datetime
from model import connect_to_db, Book, User, Page
import crud
import model
import storybookcreator
from faker import Faker

os.system('dropdb storybook')
os.system('createdb storybook')

model.connect_to_db(storybookcreator.app)
model.db.create_all()
fake = Faker()

#  Create books and users, store them in list so we can use them
book_in_db = []
user_in_db = []
page_in_book_db = []

# Create users and books 1-150
for n in range(1,10):
    
    fname = fake.first_name()
    lname = fake.last_name()
    email = f'{fname}.{lname}@test.com'  # unique emails
    password = fake.word()
    title = " ".join(fake.words())
    author_id = f"{fname} {lname}"
    # created_date = fake.date()
    
    

    user = crud.create_user(email=email, password=password, fname = fname,lname=lname)
    book = crud.create_book(email=email, title=title)

    # Create pages for book
    for m in range(1,10):
        # create 10 pages to seed each book, along with images and text.
        page_number= m
        page_image =  f'{m}.png' # A unique image!
        page_text = fake.text()
        cover_image = f'{m}.png'

        page = crud.create_book_page(page_text=page_text, page_image=page_image, email=email)
        cover_page = crud.create_cover_page(page_text=page_text, cover_image=cover_image, email=email)
        page_in_book_db.append(cover_page)
        page_in_book_db.append(page)
        

    book_in_db.append(book)
    user_in_db.append(user)
    