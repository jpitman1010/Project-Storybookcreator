"""Tables for Storybook Creator App and connection to database"""

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



def connect_to_db(flask_app, db_uri='postgresql:///storybook', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')

class User(db.Model):
    """A user. db.Model is PSQL design tool to help manage, design my database."""
    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key= True,)
    email = db.Column(db.String, unique = True,)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    password = db.Column(db.String, nullable=False)


    def __repr__(self):
        """show info about the user"""

        return f"<User ID={self.user_id} Email={self.email}, password ={self.password}, author = {self.fname}{self.lname}>"



class Book(db.Model):
    """A Book."""
    
    __tablename__ = "books"

    book_id = db.Column(db.Integer, 
                        autoincrement=True,
                        primary_key=True,)
    title = db.Column(db.String,)
    # summary = db.Column(db.text,)
    genre = db.Column(db.String,)
    # cover_img = db.Column (db.String)
    author_id = db.Column(db.Integer, 
                        primary_key=True)
 
    created_date = db.Column(db.DateTime,)



    def __repr__(self):
        """show info about the book"""

        return f"<Book ID={self.book_id} title={self.title}, author ={self.author_id}{self.author_fname}{self.author_lname}, creation date = {self.creation_date}.>"

# class Pages(db.Model):
#     """A Book."""
#     __tablename__ = "pages"

#     page_number = db.Column(db.Integer, 
#                         autoincrement=True,
#                         primary_key=True,)
#     page_text = db.Column(db.text,)
#     page_image = Column(db.String)


#     book = db.relationship('Books', backref='pages',)
#     user = db.relationship('Users', backref = 'pages',)

#     def __repr__(self):
#         """show info about the pages"""

#         return f"< Page Number = {self.page_number} page text={self.page_text}, page image = {self.page_image}.>"

    

if __name__ == '__main__':
    from storybookcreator import app
    connect_to_db(app)
    # session = session_factory()
    app.db.create_all()
    
    # Call connect_to_db(app, echo=False)
    #  if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

