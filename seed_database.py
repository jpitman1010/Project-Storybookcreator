# """Script to seed database."""

# from flask_sqlalchemy import SQLAlchemy

# import os
# import json
# from random import choice, randint
# from datetime import datetime
# from model import connect_to_db
# import model
# import crud
# import storybookcreator

# os.system('dropdb storybook')
# os.system('createdb storybook')

# model.connect_to_db(storybookcreator.app)
# model.db.create_all()


# with open('static/seeding_database_books.txt') as f:
#     book_data = text.loads(f.read())
# # Create books, store them in list so we can use them
# books_in_db = []

# for books in book_data:
#     author_id = get("author_id")
#     author_fname = get("author_fname")
#     author_lname = get("author_lname")
#     title = get("title")
#     book_id = get("book_id")
#     created_date = get("created_date")
#     author = author_fname + " " + author_lname


# new_book = crud.create_book(author, title, book_id)
# books_in_db.append(new_book)

# # Create users 1-150
# for n in range(150):
    
#     email = f'user{n}@test.com'  # unique emails
#     fname = f'FNAME{n}'
#     lname = f'LNAME{n}'
#     password = 'test'
#     user_id = f'user_id{n}'

#     user = crud.create_user(email, password)

#     # Create pages for books.
#     for m in range(1,10):

#         # make random amount of pages between 1-5
#         page_number = randint(5,10)
#         page_image =  {m}.png # A unique image!
#         page_text = f'This pages text for page {m}'
    

#         crud.create_book_pages(page_number, page_text, page_image)
