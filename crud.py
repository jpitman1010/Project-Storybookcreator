"""Server operations. CRUD = create,read,update,delete"""

from model import User,Book,Page, db
from flask import flash, redirect, render_template

def create_user(email, password,fname,lname):
    """Create and return a new user."""

    user = User(email=email, password=password, fname = fname,lname=lname)

    db.session.add(user)
    db.session.commit()

    return user

def get_users():
    """get a list of all users"""

    return db.session.query(User).all()

def get_user_id(email):
    """Return the user object by ID"""
    
    return db.session.query(User.id).filter_by(email=email).one()

def get_users_fname(email):
    """get user first name"""
    fname = db.session.query(User.fname).filter_by(email=email).first()
    fname=fname[0]
    print(fname[0])
    return fname

def get_user_by_email(email):
    """Return user email from registration"""
    user_exists_check = db.session.query(User).filter_by(email=email).first()
    return not not user_exists_check


def password_check(email, password):
    """verify that login information matches database of registered users"""
    valid_password = db.session.query(User).filter_by(password=password).first()
    return not not valid_password

def get_author_id(email):
    """get author id"""
    user =  User.query.filter_by(email = email).first()
    
    return user


def get_author_name(email):
    """get author's name"""

    fname = get_users_fname(email)
    lname= db.session.query(User.lname).filter_by(email=email).first()
    lname = lname[0]
    author= f'{fname} {lname}'

    return author


def get_book_title_list(email):
    """get list of book titles for user"""
    
    author_id = db.session.query(User.id).filter_by(email=email)
    book_title_list = db.session.query(Book.title).filter_by(author_id=author_id).all()
 
    return book_title_list

def get_book_id(title):
    """get book_ids by last book on list"""
    
    book_id = db.session.query(Book.id).filter_by(title=title).first()

    return book_id


def create_book(email, title):
    """Create a book"""
    
    author_id = db.session.query(User.id).filter_by(email=email).first()
    author = get_author_name(email)
    book_id = get_book_id(email)
    book_title_list = get_book_title_list(email)
    for last_title in book_title_list:
        title = last_title

    book = Book(author_id=author_id, title=title)

    db.session.add(book)
    db.session.commit()

    return [author, author_id, title]



def get_page_id(book_id):
    """get page_id"""

    page_id = 0
    page_id_list = db.session.query(Page.id).all()
    for last_page in page_id_list:
        page_id = last_page
    return page_id

def get_image_id(page_id):
    """get image_id"""
    image_id = db.session.query(Page.image).all()
    
    return image_id

def create_book_page(page_text, page_image, email):
    """Create a pages of book"""

    book_id = get_book_id(email)

    page = Page(text= page_text, image=page_image, book_id = book_id)
    db.session.add(page)
    db.session.commit()
    return page

def get_book_object_list(author_id):
    """get book list for updated library"""

    books = Book.query.filter_by(author_id=author_id).all()
    return books

def create_cover_page(page_text, cover_image, email):
    """Create a cover of book"""
    book_id = 0
    book_id_list = db.session.query(Book.id).all()
    for last_book in book_id_list:
        book_id = last_book
    cover_page = Page(text= page_text, cover_image=cover_image, book_id = book_id)

    db.session.add(cover_page)
    db.session.commit()

    return cover_page

def get_cover_image(email):
    """retrieve a image of book cover to display in library"""
    
    book_id = get_book_id(title)
    page_id = get_page_id(book_id)
    cover_image = db.session.query(Page.cover_image).filter_by(id=page_id).one()

    return cover_image

def get_completed_book(book_id):
    """get completed book to show in libray"""
    completed_book = db.session.query(Book).filter_by(id = book_id).all()
    completed_book = completed_book[-1]
    return  not not completed_book

def get_book_title(book_id):
    """get book title for library"""
    # title = db.session.query(Book.title).filter_by(id=book_id).first()
    book = Book.query.filter_by(id= book_id).all()
    
    return book

def check_database_for_completed_books(email):
    """checking to see if any storybooks have been completed to return library with/without books route"""
    completed_book_check = db.session.query(Book).filter_by(id = book_id).all()
    return  not not completed_book_check

def check_page_count_of_completed_book(book_id):
    """get the number of pages in a users' book to know when to stop using 'Next Page' """
    page_list = db.session.query(Page.id).filter_by(book_id=book_id).all()
    num_pages = len(page_list)
    return num_pages

def get_book_pages_by_book_id(book_id):
    """get pages of book based on book_id"""
    page_list = db.session.query(Page.id).filter_by(book_id=book_id).all()
    return page_list

def get_book_pages(book_id):
    """get pages for book"""
    # title = db.session.query(Book.title).filter_by(id=book_id).first()
    page = Page.query.filter_by(book_id= book_id).all()
    
    return page


# def get_image_by_book_and_page_id(page_id):
#     """get image from page based on page id and book id"""
    
#     page_image = db.session.query(Page.image).filter_by(page_id = page_id).all()


#     return page_image



if __name__ == '__main__':
    from storybookcreator import app
    connect_to_db(app)