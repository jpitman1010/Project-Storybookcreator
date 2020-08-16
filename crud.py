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

def get_user_by_id():
    """Return the user object by ID"""
    
    return db.session.query(User).filter_by(user_id=user_id).one()

def get_users_fname(email):
    """get a list of user first name"""
    # email = get_user_by_email(email)
    fname = db.session.query(User.fname).filter_by(email=email).all()
    # print(fname)
    return redirect('/library')

def get_user_by_email(email):
    """Return user email from regiStringation"""

    return (db.session.query(User).filter_by(email=email).first())


def check_login(email, password):
    """verify that login information matches database of registered users"""
    user = get_user_by_email(email)
    
    if user and password == user.password:
        return render_template('library.html')
    else:
        flash("Sorry, that is not a valid user login.")
        return redirect('/login')

def get_author_name(email):
    """get author's name"""

    author_fname = db.session.query(User.fname).filter_by(email=email).all()
    author_lname= db.session.query(User.lname).filter_by(email=email).all()
    author= f'{author_fname} {author_lname}'

    return author


def get_book_id():
    """get author_id"""
    
    book_id = 0
    book_id_list = db.session.query(Book.id).all()
    for last_book in book_id_list:
        book_id = last_book
    return book_id


def create_book(email):
    """Create a book"""
    
    author_id = db.session.query(User.id).filter_by(email=email).first()
    author_fname = db.session.query(User.fname).filter_by(id=author_id).all()
    author_lname = db.session.query(User.lname).filter_by(id=author_id).all()
    title = "will be updated later"
    author = f'{author_fname} {author_lname}'
    book = Book(title=title,author_id=author_id)

    db.session.add(book)
    db.session.commit()

    return author

def create_book_page(page_text, page_image, email):
    """Create a pages of book"""
    book_id = 0
    book_id_list = db.session.query(Book.id).all()
    for last_book in book_id_list:
        book_id = last_book
    page = Page(text= page_text, image=page_image, book_id = book_id)

    db.session.add(page)
    db.session.commit()

    return page

if __name__ == '__main__':
    from storybookcreator import app
    connect_to_db(app)