from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models import user

class Recipe:
    db = "recipes_schema"
    def __init__(self,data):
        self.id= data['id']
        self.name= data['name']
        self.description= data['description']
        self.instructions= data['instructions']
        self.date_cooked= data['date_cooked']
        self.under= data['under']
        self.created_at= data['created_at']
        self.updated_at= data['updated_at']
        self.user_id = data['user_id']
        self.user = None

# Create
    @classmethod
    def save_new_recipe(cls,data):
        query = "INSERT INTO recipes(name, description, instructions, date_cooked, under, user_id) VALUES(%(name)s, %(description)s, %(instructions)s, %(date_cooked)s, %(under)s, %(user_id)s);"
        results = connectToMySQL(cls.db).query_db(query,data)
        return results

# Read
    @classmethod
    def get_one_recipe(cls,id):
        data={
            'id':id
        }
        query = "SELECT * FROM recipes LEFT JOIN users ON user_id = users.id WHERE recipes.id=%(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        recipe = cls(results[0])

        user_data={
                'id': results[0]['users.id'],
                'first_name': results[0]['first_name'],
                'last_name': results[0]['last_name'],
                'email': results[0]['email'],
                'password': results[0]['password'],
                'created_at': results[0]['users.created_at'],
                'updated_at': results[0]['users.updated_at'],
        }
        recipe.user=user.User(user_data)
        return recipe

    @classmethod
    def get_recipes(cls):
        query = "SELECT * FROM recipes LEFT JOIN users ON user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        recipes = []
        for row in results:
            recipe = cls(row)

            user_data={
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
                }
            recipe.user = user.User(user_data)
            recipes.append(recipe)
        return recipes

# Update
    @classmethod
    def update_recipe(cls,data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, date_cooked=%(date_cooked)s, under=%(under)s WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return results

# Delete
    @classmethod
    def delete_recipe(cls, id):
        data={
            'id':id
        }
        query="DELETE FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return results

# Validate
    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 2:
            is_valid=False
            flash("Name must be at least 3 characters", "recipe")
        if len(recipe['description']) < 3:
            flash("Description must not be blank", "recipe")
            is_valid=False
        if len(recipe['instructions']) < 3:
            flash("Instructions must not be blank", "recipe")
            is_valid=False
        return is_valid