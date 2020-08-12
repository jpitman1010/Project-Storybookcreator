"""Script to seed database."""

from flask_sqlalchemy import SQLAlchemy

import os
import json
from random import choice, randint
from datetime import datetime
from model import connect_to_db
import model
import crud
import storybookcreator

os.system('dropdb storybook')
os.system('createdb storybook')

model.connect_to_db(storybookcreator.app)
model.db.create_all()


#  Create books and users, store them in list so we can use them
books_in_db = []
users_in_db = []

# Create users and books 1-150
for n in range(1,150):
    
    email = f'user{n}@test.com'  # unique emails
    fname = f'FNAME{n}'
    lname = f'LNAME{n}'
    password = 'test'
    user_id = n
    author_id = n
    title = f'Title{n}'
    book_id = n

    user = crud.create_user(email=email, password=password, fname = fname,lname=lname, user_id = user_id)
    print(user)
    book = crud.create_book(author_id=author_id, title=title, book_id=book_id)

    books_in_db.append(book)
    users_in_db.append(user)


    # Create pages for books.
    # for m in range(1,10):

    #     # make random amount of pages between 1-5
    #     page_number = randint(5,10)
    #     page_image =  {m}.png # A unique image!
    #     page_text = f'This pages text for page {m}'
    

    #     crud.create_book_pages(page_number, page_text, page_image)
