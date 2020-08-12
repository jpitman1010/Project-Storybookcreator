"""Server operations. CRUD = create,read,update,delete"""

from model import User,Book, db
from flask import flash, redirect

def create_user(email, password,fname,lname, user_id):
    """Create and return a new user."""

    user = User(email=email, password=password, fname = fname,lname=lname, user_id = user_id)

    db.session.add(user)
    db.session.commit()

    return user

def get_users():
    """get a list of all users"""

    return db.session.query(User).all()

def get_user_by_id(user_id):
    """Return the user object by ID"""

    return db.session.query(User).filter_by(user_id=user_id).one()

def get_user_by_email(email):
    """Return user email from registration"""

    return (db.session.query(User).filter_by(email=email).first())


def check_login(email, password):
    """verify that login information matches database of registered users"""
    user = get_user_by_email(email)
    
    if user:
        return password == user.password
    else:
        flash("Sorry, that is not a valid user login.")
        return redirect('/')

def create_book(author_id,title, book_id):
    """Create a books"""

    book = Book(author_id = author_id,title=title, book_id= book_id)

    db.session.add(book)
    db.session.commit()


    return book

# def create_book_pages(page_number, page_text, page_image):
#     """Create a pages of book"""

#     pages = Pages(page_number = page_number, page_text= page_text, page_image=page_image)

#     db.session.add(pages)
#     db.session.commit()

#     return pages


        
if __name__ == '__main__':
    from storybookcreator import app
    # connect_to_db(app)