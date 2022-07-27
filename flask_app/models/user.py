from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class User:
    db = 'recipes_schema'
    def __init__(self,data):
        self.id= data['id']
        self.first_name= data['first_name']
        self.last_name= data['last_name']
        self.email= data['email']
        self.password= data['password']
        self.created_at= data['created_at']
        self.updated_at= data['updated_at']

# Create
    @classmethod
    def save_new_user(cls,data):
        query = "INSERT INTO users(first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        results = connectToMySQL(cls.db).query_db(query,data)
        return results

#Read
    @classmethod
    def get_by_id(cls,data):
        query= "SELECT * FROM users WHERE id=%(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])  

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email=%(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])  

#Update

#Delete


# Validate
    @staticmethod
    def validate_register(user):
        query = "SELECT * FROM users WHERE email=%(email)s;"
        results = connectToMySQL(User.db).query_db(query,user)
            # can't use (cls.db) or (query,data) because it's not a class method and we're not passing data, we're passing owner info specifically

        is_valid = True
        if len(results) >=1:
            flash("Email already associated with an account!","register")
            is_valid = False
        if len(user['first_name']) < 3:
            flash("First name must have at least 3 characters!", "register")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must have at least 3 characters!", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must have at least 8 characters!","register")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords don't match", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email format","register")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(user):
        query = "SELECT * FROM users WHERE email=%(email)s;"
        results = connectToMySQL(User.db).query_db(query,user)
        is_valid = True

        if not results:
            flash('Invalid email or password', 'login')
            is_valid = False
        elif not bcrypt.check_password_hash(User(results[0]).password, user['password']):
            flash("Invalid email or password","login")
            is_valid = False
        return is_valid