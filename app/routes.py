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

@app.route("/account_info")
def account_info():
    items = db_helper.fetch_tastemaker()
    return render_template("account_info.html", items=items)

@app.route("/view_lists")
def view_lists():
    items = db_helper.fetch_personal_lists()
    return render_template("personal_lists.html", items=items)

@app.route("/view_lists/create_new_list", methods=['GET'])
def create_new_list(name):
    if request.method == 'GET':
        default = 'empty'
        data = request.form.get('list_name', default)
        if data == "" or data == default:
            return render_template("personal_lists.html")
        db_helper.create_list(data)
        items = db_helper.fetch_personal_lists()
        return render_template("personal_lists.html", items=items)
    return render_template("personal_lists.html", items=items)

@app.route("/userhome")
def userhome():
    # is this right?
    items = db_helper.add_user() 
    return render_template("user_home.html")


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


@app.route("/recipesearch")
def recipeSearch():
    return render_template("recipe_search.html", items=[])

@app.route("/hello", methods = ['GET', 'POST'])
def hello():
    print(request.method)
    if request.method == 'POST':
        #print(request.form['search_entry'])
        default = 'empty'
        data = request.form.get('search_entry', default)
        print(data)
        if data == "" or data == default:
            return render_template("recipe_search.html")
        items = db_helper.fetch_recipe_by_name(data)
        return render_template("recipe_search.html", items=items)
    return render_template("login.html", items=[])

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

@app.route('/recipesearch/<id>')
def get_recipe(id):
    print(id)
    recipe_info = db_helper.fetch_recipe(id)
    return render_template("recipe.html", items=recipe_info)

# @app.route()
# @app.roue("/recipesearch/<id>"):
# @app.route('/recipe')
# def profile():
#     return '{}\'s profile'.format(escape(username))")
