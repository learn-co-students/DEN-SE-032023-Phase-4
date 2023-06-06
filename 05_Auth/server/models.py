# imports
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
#5 )pip install flask_bcrypt and import bcrypt and wrap the app in bcrypt, import hybrid property
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
bcrypt = Bcrypt()
metadata = MetaData(naming_convention={
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_`%(constraint_name)s`",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
    })

db = SQLAlchemy(metadata=metadata)

class User(db.Model,SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique = True)
    _password_hash = db.Column(db.String)
    # 6) add the password hash, db revision, and upgrade head
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Create a get method using hybrid property
    @hybrid_property
    def password_hash(self):
        return self._password_hash
    #Create a setter method to set the password
    @password_hash.setter
    def password(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    #Create an authentication method to check the password
    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))

