import os
from flask import Flask, render_template, redirect, request, url_for, session, Blueprint
from flask_pymongo import PyMongo, pymongo#
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'cookbook-database'
app.config['MONGO_URI'] = "mongodb://admin1234:admin1234@ds233238.mlab.com:33238/cookbook-database"
mongo = PyMongo(app)

@app.route('/home')
def home():
    return render_template('home.html')
    
@app.route('/cookbook', methods=["POST","GET"])
def get_cookbook():
    offset= 1
    return render_template('recipes/food.html',
    offset = offset,
    continents = mongo.db.continents.find(),
    allergies = mongo.db.allergies.find(),
    foods = mongo.db.foods.find(),
    recipes = mongo.db.recipes.find().sort('recipe_name', pymongo.ASCENDING).limit(4))
    
@app.route('/add_recipe')
def add_recipe():
    return render_template('recipes/add_recipe.html', 
    allergies = mongo.db.allergies.find(),
    continents = mongo.db.continents.find(),
    foods = mongo.db.foods.find())
    
@app.route('/insert_recipe', methods=["POST"])
def insert_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one(
    {
        'continent_name': request.form.get("continent_name"),
        'recipe_name': request.form.get("recipe_name"),
        'food_type': request.form.get("food_type"),
        'recipe_time': request.form.get('recipe_time'),
        'recipe_servings': request.form.get('recipe_servings'),
        'recipe_ingredients': request.form.get('recipe_ingredients'),
        'recipe_instructions1': request.form.get('recipe_instructions1'),
        'recipe_instructions2': request.form.get('recipe_instructions2'),
        'recipe_instructions3': request.form.get('recipe_instructions3'),
        'recipe_instructions4': request.form.get('recipe_instructions4'),
        'allergy_name': request.form.get('allergy_name'),
        'likes': 0,
        'dislikes': 0
    })
    return redirect(url_for('get_cookbook'))
    
@app.route('/view_recipe/<recipe_id>', methods=["POST", "GET"])
def view_recipe(recipe_id):
    voted = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)},
        {
            "likes" : 1,
            'dislikes': 1
        })
    vote_storage = []
    vote_storage.append(voted)
    if request.method == "POST":
        if request.form['likesdislikes'] == "like":
            likes = vote_storage[0]["likes"] + 1
            mongo.db.recipes.update_one({'_id': ObjectId(recipe_id) }, { '$set' : { "likes" : likes}})
            return redirect(url_for('get_cookbook'))
        elif request.form['likesdislikes'] == "dislike":
            dislikes = vote_storage[0]['dislikes'] + 1
            mongo.db.recipes.update_one( {'_id': ObjectId(recipe_id) },  {'$set': { 'dislikes' : dislikes }} )
            return redirect(url_for('get_cookbook'))
    return render_template('recipes/viewrecipe.html',
    recipes = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)}))
    
@app.route('/edit_recipe/<recipe_name>')
def edit_recipe(recipe_name):
    recipes = mongo.db.recipes.find_one({"_id": ObjectId(recipe_name)})
    return render_template('recipes/editrecipe.html', 
    continents = mongo.db.continents.find(),
    foods = mongo.db.foods.find(),
    allergies = mongo.db.allergies.find(),
    recipes=recipes)
    
@app.route('/update_recipe/<recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    recipe = mongo.db.recipes
    recipe.update({"_id": ObjectId(recipe_id)},
    {
        'continent_name': request.form.get("continent_name"),
        'recipe_name': request.form.get("recipe_name"),
        'food_type': request.form.get("food_type"),
        'recipe_time': request.form.get('recipe_time'),
        'recipe_servings': request.form.get('recipe_servings'),
        'recipe_ingredients': request.form.get('recipe_ingredients'),
        'recipe_instructions1': request.form.get('recipe_instructions1'),
        'recipe_instructions2': request.form.get('recipe_instructions2'),
        'recipe_instructions3': request.form.get('recipe_instructions3'),
        'recipe_instructions4': request.form.get('recipe_instructions4'),
        'allergy_name': request.form.get('allergy_name'),
        'likes': 0,
        'dislikes': 0
    })
    return redirect(url_for('get_cookbook'))
    
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({"_id":ObjectId(recipe_id)})
    return redirect(url_for('get_cookbook'))
    
@app.route('/allergies')
def allergies():
    return render_template('allergies/allergies.html',
    count = mongo.db.allergies.find().count(),
    allergies = mongo.db.allergies.find())
    
@app.route('/new_allergy')
def new_allergy():
    return render_template('allergies/addallergy.html', 
    allergies = mongo.db.allergies.find())
    
@app.route('/insert_allergy', methods=["POST"])
def insert_allergy():
    allergies = mongo.db.allergies
    allergies.insert_one(request.form.to_dict())
    return redirect(url_for('allergies'))
    
@app.route('/delete_allergy/<allergy_name>')
def delete_allergy(allergy_name):
    mongo.db.allergies.remove({"_id": ObjectId(allergy_name)})
    return redirect(url_for('allergies'))
    
@app.route('/europe')
def europe():
    offset= 1
    return render_template('continents/europe.html',
    offset = offset,
    count = mongo.db.recipes.find({"continent_name" : "Europe"}).count(),
    recipes = mongo.db.recipes.find({"continent_name" : "Europe"}).sort('recipe_name', pymongo.ASCENDING).limit(4))
    
@app.route('/namerica')
def namerica():
    offset = 1
    return render_template('continents/namerica.html',
    offset = offset,
    count = mongo.db.recipes.find({"continent_name" : "North America"}).count(),
    recipes = mongo.db.recipes.find({"continent_name" : "North America"}).sort('recipe_name', pymongo.ASCENDING).limit(4))

@app.route('/samerica')
def samerica():
    offset = 1
    return render_template('continents/samerica.html',
    offset = offset,
    count = mongo.db.recipes.find({"continent_name" : "South America"}).count(),
    recipes = mongo.db.recipes.find({"continent_name" : "South America"}).sort('recipe_name', pymongo.ASCENDING).limit(4))
    
@app.route('/asia')
def asia():
    offset = 1
    return render_template('continents/asia.html',
    offset = offset,
    count = mongo.db.recipes.find({"continent_name" : "Asia"}).count(),
    recipes = mongo.db.recipes.find({"continent_name" : "Asia"}).sort('recipe_name', pymongo.ASCENDING).limit(4))
    
@app.route('/africa')
def africa():
    offset = 1
    return render_template('continents/africa.html',
    offset = offset,
    count = mongo.db.recipes.find({"continent_name" : "Africa"}).count(),
    recipes = mongo.db.recipes.find({"continent_name" : "Africa"}).sort('recipe_name', pymongo.ASCENDING).limit(4))
    
@app.route('/australia')
def australia():
    offset = 1
    return render_template('continents/australia.html',
    offset = offset,
    count = mongo.db.recipes.find({"continent_name" : "Australia"}).count(),
    recipes = mongo.db.recipes.find({"continent_name" : "Australia"}).sort('recipe_name', pymongo.ASCENDING).limit(4))

@app.route('/chicken')
def chicken():
    offset = 1
    return render_template('foodtype/chicken.html',
    offset = offset,
    count = mongo.db.recipes.find({"food_type" : "Chicken"}).count(),
    recipes = mongo.db.recipes.find({"food_type" : "Chicken"}).sort('recipe_name', pymongo.ASCENDING).limit(4))
    
@app.route('/beef')
def beef():
    offset = 1
    return render_template('foodtype/beef.html',
    offset = offset,
    count = mongo.db.recipes.find({"food_type" : "Beef"}).count(),
    recipes = mongo.db.recipes.find({"food_type" : "Beef"}).sort('recipe_name', pymongo.ASCENDING).limit(4))

@app.route('/lamb')
def lamb():
    offset = 1
    return render_template('foodtype/lamb.html',
    offset = offset,
    count = mongo.db.recipes.find({"food_type" : "Lamb"}).count(),
    recipes = mongo.db.recipes.find({"food_type" : "Lamb"}).sort('recipe_name', pymongo.ASCENDING).limit(4))
    
@app.route('/pork')
def pork():
    offset = 1
    return render_template('foodtype/pork.html',
    offset = offset,
    count = mongo.db.recipes.find({"food_type" : "Pork"}).count(),
    recipes = mongo.db.recipes.find({"food_type" : "Pork"}).sort('recipe_name', pymongo.ASCENDING).limit(4))
    
@app.route('/fish')
def fish():
    offset = 1
    return render_template('foodtype/fish.html',
    offset = offset,
    count = mongo.db.recipes.find({"food_type" : "Fish"}).count(),
    recipes = mongo.db.recipes.find({"food_type" : "Fish"}).sort('recipe_name', pymongo.ASCENDING).limit(4))
    
@app.route('/vegetarian')
def vegetarian():
    offset = 1
    return render_template('foodtype/vegetarian.html',
    offset = offset,
    count = mongo.db.recipes.find({"food_type" : "Vegetarian"}).count(),
    recipes = mongo.db.recipes.find({"food_type" : "Vegetarian"}).sort('recipe_name', pymongo.ASCENDING).limit(4))
    
@app.route('/vegan')
def vegan():
    offset = 1
    return render_template('foodtype/vegan.html',
    offset = offset,
    count = mongo.db.recipes.find({"food_type" : "Vegan"}).count(),
    recipes = mongo.db.recipes.find({"food_type" : "Vegan"}).sort('recipe_name', pymongo.ASCENDING).limit(4))