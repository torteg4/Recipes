from flask import render_template,redirect,session,request,flash
from flask_app import app
from flask_app.models import user, recipe


@app.route("/recipe/<int:id>")
def show_recipe(id):
    return render_template("show_recipe.html", recipe=recipe.Recipe.get_one_recipe(id))

@app.route("/recipe/edit/<int:id>")
def edit_recipe(id):
    return render_template("edit_recipe.html", recipe=recipe.Recipe.get_one_recipe(id))

@app.route("/recipe/update", methods=["POST"])
def update_recipe():
    if not recipe.Recipe.validate_recipe(request.form):
        return redirect(f"/recipe/edit/{request.form['id']}")
        
    recipe.Recipe.update_recipe(request.form)
    return redirect(f"/recipe/{request.form['id']}")

@app.route("/delete/<int:id>", methods =['POST'])
def delete_pet(id):
    recipe.Recipe.delete_recipe(id)
    return redirect('/dashboard')
