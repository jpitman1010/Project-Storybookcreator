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

def create_book(author,title, book_id):
    """Create a books"""

    book_id = db.sessoin.query(Book).filter_by(book_id=book_id).last()
    book = Book(author= author,title=title)

    db.session.add(book)
    db.session.commit()

    return book

def create_book_page(page_number, page_text, page_image, book_id):
    """Create a pages of book"""

    number = db.session.query(Page).filter_by(book_id=book_id).last()
    page = Page(number = page_number, text= page_text, image=page_image, book_id = book_id)

    db.session.add(page)
    db.session.commit()

    return page

if __name__ == '__main__':
    from storybookcreator import app
    # connect_to_db(app)