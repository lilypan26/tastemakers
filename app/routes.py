""" Specifies routing for the application"""
from flask import render_template, request, jsonify
from app import app
from app import database as db_helper

# @app.route("/delete/<int:task_id>", methods=['POST'])
# def delete(task_id):
#     """ recieved post requests for entry delete """

#     try:
#         db_helper.remove_task_by_id(task_id)
#         result = {'success': True, 'response': 'Removed task'}
#     except:
#         result = {'success': False, 'response': 'Something went wrong'}

#     return jsonify(result)


# @app.route("/edit/<int:task_id>", methods=['POST'])
# def update(task_id):
#     """ recieved post requests for entry updates """

#     data = request.get_json()

#     try:
#         if "status" in data:
#             db_helper.update_status_entry(task_id, data["status"])
#             result = {'success': True, 'response': 'Status Updated'}
#         elif "description" in data:
#             db_helper.update_task_entry(task_id, data["description"])
#             result = {'success': True, 'response': 'Task Updated'}
#         else:
#             result = {'success': True, 'response': 'Nothing Updated'}
#     except:
#         result = {'success': False, 'response': 'Something went wrong'}

#     return jsonify(result)

# 
# @app.route("/create", methods=['POST'])
# def create():
#     """ recieves post requests to add new task """
#     data = request.get_json()
#     db_helper.insert_new_task(data['description'])
#     result = {'success': True, 'response': 'Done'}
#     return jsonify(result)


@app.route("/")
def homepage():
    #items = db_helper.fetch_tastemaker()
    return render_template("login.html")

@app.route("/grocery")
def grocery():
    items = db_helper.fetch_tastemaker()
    return render_template("index.html", items=items)

@app.route("/view_lists")
def view_lists():
        #print(request.form['search_entry'])
    items = db_helper.fetch_lists()
    return render_template("personal_lists.html", items=items)

# @app.route("/view_lists/create_new_list", methods=['POST', 'GET'])
# def create_new_list(name):
#     if request.method == 'POST':
#         default = 'empty'
#         data = request.form.get('list_name', default)
#         if data == "" or data == default:
#             return render_template("personal_lists.html")
#         db_helper.create_list(data)
#         items = db_helper.fetch_personal_lists()
#         return render_template("personal_lists.html", items=items)
#     return render_template("personal_lists.html", items=items)

@app.route("/view_lists/add", methods=["POST", "GET"])
def listAdd():
    if request.method == 'POST':
        #print(request.form['search_entry'])
        default = 'empty'
        data = request.form.get('search_entry', default)
        print(data)
        if data == "" or data == default:
            return render_template("personal_lists.html")
        items = db_helper.add_list_by_name(data)
        return render_template("personal_lists.html", items=items)
    return render_template("personal_lists.html")


@app.route("/view_lists/update", methods = ['POST'])
def listSearch():
    if request.method == 'POST':
        old = request.form['old_entry']
        new = request.form['new_entry']
        default = 'empty'
        if old == "" or old == default:
            render_template("personal_lists.html")
        items = db_helper.update_list_entry(old, new)
        return render_template("personal_lists.html", items=items)
    return render_template("personal_lists.html")

@app.route("/view_lists/delete", methods=["POST", "GET"])
def listDelete():
    if request.method == 'POST':
        #print(request.form['search_entry'])
        default = 'empty'
        data = request.form.get('search_entry', default)
        print(data)
        if data == "" or data == default:
            return render_template("personal_lists.html")
        items = db_helper.delete_list_by_name(data)
        return render_template("personal_lists.html", items=items)
    return render_template("personal_lists.html")
############################################# Stored Procedure ###############################################
 
@app.route("/recipesearch/get_difficulty", methods=["POST", "GET"])
def get_difficulty():
    difficulty_results = db_helper.fetch_difficulty()
    return render_template("difficulty.html", items=difficulty_results)  
##################################################################################################################

#Delete ingredient_name FROM Recipes WHERE ingredient_name IN (SELECT ingredient_name 
# FROM RecipeHasIngredients )
@app.route("/recipesearch/add_ingredient", methods=["POST", "GET"])
def ingredient_add():
    if request.method == 'POST':
        #print(request.form['search_entry'])
        default = 'empty'
        recipe_id = request.form.get('recipe_id', default)
        ingredient = request.form.get('ingredient', default)
        if recipe_id == "" or recipe_id == default:
            return render_template("recipe_search.html")
        db_helper.add_ingredient_by_name(recipe_id, ingredient)
        return render_template("recipe_search.html")
    return render_template("recipe_search.html")  


@app.route("/recipesearch/delete_ingredient", methods=["POST", "GET"])
def ingredient_remove():
    if request.method == 'POST':
        #print(request.form['search_entry'])
        default = 'empty'
        recipe_id = request.form.get('recipe_id', default)
        ingredient = request.form.get('ingredient', default)
        if recipe_id == "" or recipe_id == default:
            return render_template("recipe_search.html")
        db_helper.delete_ingredient(recipe_id, ingredient)
        return render_template("recipe_search.html")
    return render_template("recipe_search.html")  

@app.route("/recipesearch/update_ingredient", methods=["POST", "GET"])
def ingredient_update():
    if request.method == 'POST':
        #print(request.form['search_entry'])
        default = 'empty'
        recipe_id = request.form.get('recipe_id', default)
        ingredient_old = request.form.get('ingredient_old', default)
        ingredient_new = request.form.get('ingredient_new', default)
        if recipe_id == "" or recipe_id == default:
            return render_template("recipe_search.html")
        db_helper.update_ingredient(recipe_id, ingredient_old, ingredient_new)
        return render_template("recipe_search.html")
    return render_template("recipe_search.html")  

#Delete ingredient_name FROM Recipes WHERE ingredient_name IN (SELECT ingredient_name 
# FROM RecipeHasIngredients )
@app.route("/recipesearch/add_tag", methods=["POST", "GET"])
def tag_add():
    if request.method == 'POST':
        #print(request.form['search_entry'])
        default = 'empty'
        recipe_id = request.form.get('recipe_id', default)
        tag = request.form.get('tag', default)
        if recipe_id == "" or recipe_id == default:
            return render_template("recipe_search.html")
        db_helper.add_tag_by_name(recipe_id, tag)
        return render_template("recipe_search.html")
    return render_template("recipe_search.html")  

@app.route("/recipesearch/delete_tag", methods=["POST", "GET"])
def tag_remove():
    if request.method == 'POST':
        #print(request.form['search_entry'])
        default = 'empty'
        recipe_id = request.form.get('recipe_id', default)
        tag = request.form.get('tag', default)
        if recipe_id == "" or recipe_id == default:
            return render_template("recipe_search.html")
        db_helper.delete_tag(recipe_id, tag)
        return render_template("recipe_search.html")
    return render_template("recipe_search.html")  

@app.route("/recipesearch/update_tag", methods=["POST", "GET"])
def tag_update():
    if request.method == 'POST':
        #print(request.form['search_entry'])
        default = 'empty'
        recipe_id = request.form.get('recipe_id', default)
        tag_old = request.form.get('tag_old', default)
        tag_new = request.form.get('tag_new', default)
        if recipe_id == "" or recipe_id == default:
            return render_template("recipe_search.html")
        db_helper.update_tag(recipe_id, tag_old, tag_new)
        return render_template("recipe_search.html")
    return render_template("recipe_search.html")  
# @app.route("/recipe_search/add", methods=["POST", "GET"])
# def recipeAdd():
#     if request.method == 'POST':
#         #print(request.form['search_entry'])
#         default = 'empty'
#         name = request.form.get('name_entry', default)
#         sugar = request.form.get('sugar_entry', default)
#         num_steps = request.form.get('num_step_entry', default)
#         steps_text = request.form.get('step_text_entry', default)
#         minutes = request.form.get('minutes_entry', default)
#         contributor_id = request.form.get('contributor_entry', default)
#         sodium = request.form.get('sodium_entry', default)
#         total_fat = request.form.get('fat_entry', default)
#         saturated_fat = request.form.get('saturated_entry', default)
#         calories = request.form.get('calories_entry', default)
#         protein = request.form.get('protein_entry', default)

#         if name == "" or name == default:
#             return render_template("recipe_search.html")
#         items = db_helper.add_recipe_by_name(minutes, num_steps, steps_text, contributor_id, name, sugar, sodium, protein, total_fat, saturated_fat, calories)
#         return render_template("recipe_search.html", items=items)
#     return render_template("recipe_search.html")

# @app.route("/recipe_search/delete", methods=["POST", "GET"])
# def recipeDelete():
#     if request.method == 'POST':
#         #print(request.form['search_entry'])
#         default = 'empty'
#         data = request.form.get('search_entry', default)
#         print(data)
#         if data == "" or data == default:
#             return render_template("recipe_search.html")
#         items = db_helper.delete_recipe_by_name(data)
#         return render_template("recipe_search.html", items=items)
#     return render_template("recipe_search.html")

# @app.route("/recipe_search/update", methods = ['POST'])
# def recipeUpdate():
#     if request.method == 'POST':
#         old = request.form['old_entry']
#         new = request.form['new_entry']
#         default = 'empty'
#         if old == "" or old == default:
#             render_template("recipe_search.html")
#         items = db_helper.update_recipe_entry(old, new)
#         return render_template("recipe_search.html", items=items)
#     return render_template("recipe_search.html")

@app.route("/userhome")
def userhome():
    # is this right?
    #items = db_helper.add_user() 
    return render_template("user_home.html")

# @app.route("/account_info/create", methods=['POST'])
# def add_user(name):
#     if request.method == 'POST':
#         default = 'empty'
#         username = request.form.get('user_entry', default)
#         email = request.form.get('email_entry', default)
#         password = request.form.get('password_entry', default)
#         name = request.form.get('name_entry', default)
#         if name == "" or name == default:
#             return render_template("user.html")
#         #db_helper.create_list(data)
#         db_helper.add_user(username, email, password, name)
#         return render_template("user.html", items=[])
#     return render_template("user.html", items=[])
@app.route("/account_info")
def account_info():
    items = db_helper.fetch_users()
    return render_template("user.html", items=items)

@app.route("/account_info/create", methods=['POST'])
def add_user():
    if request.method == 'POST':
        default = 'empty'
        username = request.form.get('user_entry', default)
        email = request.form.get('email_entry', default)
        password = request.form.get('password_entry', default)
        name = request.form.get('name_entry', default)
        if name == "" or name == default:
            return render_template("user.html")
        #db_helper.create_list(data)
        items = db_helper.add_user(username, name, email, password)
        return render_template("user.html", items=items)
    return render_template("user.html", items=[])


@app.route("/account_info/update", methods = ['POST'])
def userUpdate():
    if request.method == 'POST':
        old = request.form['old_entry']
        new = request.form['new_entry']
        default = 'empty'
        if old == "" or old == default:
            render_template("user.html")
        items = db_helper.update_user_entry(old, new)
        return render_template("user.html", items=items)
    return render_template("user.html")


@app.route("/account_info/delete", methods=['POST'])
def delete_user():
    if request.method == 'POST':
        default = 'empty'
        username = request.form.get('user_id_to_delete', default)
        if username == "" or username == default:
            return render_template("user.html")
        #db_helper.create_list(data)
        items = db_helper.delete_user(username)
        return render_template("user.html", items=items)
    return render_template("user.html", items=[])
# @app.route('/user/<username>')
# def profile(username):
#     return '{}\'s profile'.format(escape(username))")
# @app.route("/login")
# def login():

# @app.route("/logout")
# def logout():

# @app.route("/tomake")
# def tomake();

# @app.route("/grocery")
# def grocery():

# @app.route("/favorites")
# def favorites():

# @app.route('/login', methods = ['GET', 'POST'])


@app.route("/recipesearch", methods=["POST", "GET"])
def recipeSearch():
    if request.method == 'POST':
        #print(request.form['search_entry'])
        default = 'empty'
        data = request.form.get('search_entry', default)
        print(data)
        if data == "" or data == default:
            return render_template("recipe_search.html")
        items = db_helper.fetch_recipe_by_name(data)
        return render_template("recipe_search.html", items=items)
    return render_template("recipe_search.html")

@app.route("/recipesearch/tomoko")
def recipeSearchResults():
    tomoko_results = db_helper.fetch_tomoko()
    return render_template("recipe_search.html", items=tomoko_results)

@app.route("/recipesearch/teresa")
def recipeSearchResults_teresa():
    print("here")
    teresa_results = db_helper.fetch_teresa()
    return render_template("recipe_search.html", items=teresa_results)
    
@app.route("/recipesearch/swathi")
def recipeSearchResults_swathi():
    swathi_results = db_helper.fetch_swathi()
    return render_template("recipe_search.html", items=swathi_results)

@app.route("/recipesearch/healthy")
def healthyRecipes():
    healthy_results = db_helper.fetch_healthy()
    return render_template("recipe_search.html", items=healthy_results)

@app.route("/recipesearch/tag_search", methods = ['GET', 'POST'])
def tag_search():
    print(request.method)
    if request.method == 'POST':
        #print(request.form['search_entry'])
        default = 'empty'
        data = request.form.get('tag_entry', default)
        print(data)
        if data == "" or data == default:
            return render_template("recipe_search.html")
        items = db_helper.fetch_recipe_by_tag(data)
        return render_template("recipe_search.html", items=items)
    return render_template("recipe_search.html", items=[])

@app.route("/recipesearch/time_search", methods = ['GET', 'POST'])
def time_search():
    print(request.method)
    if request.method == 'POST':
        #print(request.form['search_entry'])
        default = 'empty'
        data = request.form.get('time_entry', default)
        print(data)
        if data == "" or data == default:
            return render_template("recipe_search.html")
        items = db_helper.fetch_recipe_by_time(data)
        return render_template("recipe_search.html", items=items)
    return render_template("recipe_search.html", items=[])

# @app.route("/recipesearch/ingredient_search", methods = ['GET', 'POST'])
# def ingredient_search():
#     print(request.method)
#     if request.method == 'POST':
#         #print(request.form['search_entry'])
#         default = 'empty'
#         data = request.form.get('search_entry', default)
#         print(data)
#         if data == "" or data == default:
#             return render_template("recipe_search.html")
#         items = db_helper.fetch_recipe_by_name(data)
#         return render_template("recipe_search.html", items=items)
#     return render_template("recipe_search.html", items=[])
    
@app.route("/recipesearch/num_ingr_search", methods = ['GET', 'POST'])
def num_ingr_search():
    print(request.method)
    if request.method == 'POST':
        #print(request.form['search_entry'])
        default = 'empty'
        data = request.form.get('ingr_entry', default)
        print(data)
        if data == "" or data == default:
            return render_template("recipe_search.html")
        items = db_helper.fetch_recipe_by_num_ingr(data)
        return render_template("recipe_search.html", items=items)
    return render_template("recipe_search.html", items=[])
    
@app.route('/recipesearch/<id>')
def get_recipe(id):
    recipe_info = db_helper.fetch_recipe(id)
    return render_template("recipe.html", recipe=recipe_info)

# @app.route()
# @app.roue("/recipesearch/<id>"):
# @app.route('/recipe')
# def profile():
#     return '{}\'s profile'.format(escape(username))")
