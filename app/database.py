"""Defines all the functions related to the database"""
from app import db
from app import settings
from sqlalchemy.sql import func
from sqlalchemy import DDL, event
from sqlalchemy.ext.compiler import compiles
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from ast import literal_eval
# from app import other_db
# from flask_sqlalchemy import SQLAlchemy
def fetch_difficulty() -> list:
    conn = db.connect()
    query_results = conn.execute(text("CALL Result(:param)"), param='difficulty').fetchall()
    
    #print(query_results)
    conn.close()
    recipe_list = []
    for result in query_results[:15]:
        item = {
            "id": result[0],
            "name": result[1],
            "difficulty" : result[2]
            # "status": result[2]
        }
        recipe_list.append(item)
    #print(recipe_list)
    return recipe_list

def fetch_tastemaker() -> list:
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute("Select * from Recipe LIMIT 15;").fetchall()
    #print(query_results)
    conn.close()
    recipe_list = []
    for result in query_results:
        item = {
            "id": result[0],
            "name": result[5],
            # "status": result[2]
        }
        recipe_list.append(item)
    #print(recipe_list)
    return recipe_list

def fetch_swathi() -> list:
    conn = db.connect()

    query_results = conn.execute(text("CALL Result(:param)"), param='swathi').fetchall()
    
    # query_results = conn.execute("(SELECT r.recipe_id, r.name, COUNT(ingredient_id) as num_ingredients " +
    #                             "FROM RecipeHasIngredients rhi natural join Recipe r " +
    #                             "WHERE r.name LIKE '5 minute%%' AND rhi.recipe_id IN (SELECT recipe_id FROM Review GROUP BY recipe_id HAVING avg(rating) > 3) " +
    #                             "GROUP BY r.name " +
    #                             "HAVING num_ingredients < 8 " +
    #                             "ORDER BY num_ingredients ASC, r.name ASC) LIMIT 15;").fetchall()
    #print("query results: " + query_results)
    conn.close()
    recipes = []
    for result in query_results[:15]:
        #print("result: " + result)
        item = {
            "id": result[0],
            "name": result[1]
        }
        # print("result 0: " + str(result[0]))
        # print("result 1: " + str(result[1]))
        #print("item: " + item)
        recipes.append(item)
    return recipes

def fetch_recipe(id) -> list:
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """
    recipe_id = int(id)
    conn = db.connect()
    query_results = conn.execute("Select * from Recipe  r WHERE r.recipe_id = %s;", recipe_id).fetchall()
    ing_res = conn.execute("Select ingredient_id FROM RecipeHasIngredients WHERE recipe_id = {}".format(recipe_id)).fetchall()
    tag_res = conn.execute("Select tag_name FROM RecipeHasTags WHERE recipe_id = {}".format(recipe_id)).fetchall()
    conn.close()
    ingredients = []
    for i in ing_res:
        ingredients.append(get_ingredient_name(i[0]))
    
    tags = []
    for t in tag_res:
        tags.append(t[0])
     
    recipe = None
    for result in query_results:
        # parse json formatted list
        steps = literal_eval(result[3])
        recipe =  Recipe(result[0], result[1], result[2], steps, result[4], result[5], result[6], result[7], result[8], result[9], result[10], result[11], result[12], ingredients, tags)

    # print(recipe_list)
    return recipe
    
def fetch_healthy() -> list:
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute(text("CALL Result(:param)"), param='healthy').fetchall()
    
    # query_results = conn.execute("(SELECT r.recipe_id, r.name, r.calories as Calories " +
    #                             "FROM Recipe r JOIN RecipeHasTags rt ON r.recipe_id = rt.recipe_id " + 
    #                             "WHERE rt.tag_name = 'healthy' OR rt.tag_name = 'very-low-carbs' AND r.recipe_id IN (SELECT recipe_id FROM Review GROUP BY recipe_id HAVING COUNT(rating) > 4) " +
    #                             "GROUP BY r.recipe_id) " + 
    #                             "UNION " + 
    #                             "(SELECT r.recipe_id, r.name, r.calories as Calories " +
    #                             "FROM Recipe r JOIN RecipeHasTags rt ON r.recipe_id = rt.recipe_id " +
    #                             "WHERE r.sugar < 50 AND rt.tag_name = 'desserts' AND r.recipe_id IN (SELECT recipe_id FROM Review GROUP BY recipe_id HAVING AVG(rating) > 2)) LIMIT 15;").fetchall()
    #print(query_results)
    conn.close()
    recipe_list = []
    for result in query_results[:15]:
        item = {
            "id": result[0],
            "name": result[1],
            # "status": result[2]
        }
        recipe_list.append(item)
    #print(recipe_list)
    return recipe_list


def fetch_tomoko() -> list:
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    # qry = db.session.query()
    query_results = conn.execute("SELECT r.recipe_id, r.name " +
                                 "FROM Recipe r " + 
                                 "NATURAL JOIN RecipeHasIngredients rhi " +
                                                "NATURAL JOIN Ingredients i "+
                                 "WHERE i.ingredient_name LIKE '%%lettuce%%' AND r.recipe_id IN (SELECT recipe_id FROM RecipeHasTags WHERE tag_name LIKE 'easy') "+
                                 "ORDER BY r.name " +
                                 "LIMIT 15;").fetchall()

    conn.close()
    recipe_list = []
    for result in query_results:
        item = {
            "id": result[0],
            "name": result[1]
            # "task": result[1],
            # "status": result[2]
        }
        recipe_list.append(item)

    return recipe_list

def fetch_teresa() -> list:
    conn = db.connect()
    # qry = db.session.query()
    query_results = conn.execute("SELECT recipe_id, name, tag_count " +
                                 "FROM Recipe NATURAL JOIN (SELECT recipe_id, COUNT(tag_name) as tag_count FROM RecipeHasTags GROUP BY recipe_id) AS RecipeTagCount " + 
                                 "WHERE tag_count = 10 " +
                                 "LIMIT 15;").fetchall()
    print(query_results)
    conn.close()
    recipe_list = []
    for result in query_results:
        item = {
            "id": result[0],
            "name": result[1]
            # "task": result[1],
            # "status": result[2]
        }
        recipe_list.append(item)

    return recipe_list

def fetch_recipe_by_name(name) -> list:
    conn = db.connect()
    query_results = conn.execute("SELECT recipe_id, name FROM Recipe WHERE name LIKE '%%{}%%';".format(name)).fetchall()

    conn.close()
    recipe_list = []
    for result in query_results:
        item = {
            "id": result[0],
            "name": result[1],
        }
        recipe_list.append(item)

    return recipe_list

def fetch_recipe_by_tag(tag_name) -> list:
    conn = db.connect()
    #SELECT name FROM Recipe WHERE recipe_id IN (SELECT recipe_id from Tags WHERE tag_name LIKE “”
    query_results = conn.execute("SELECT recipe_id, name FROM Recipe WHERE recipe_id IN (SELECT recipe_id FROM Tags WHERE tag_name LIKE '%%{}%%') LIMIT 20;".format(tag_name)).fetchall()
    conn.close()
    print("recipe by tag")
    recipe_list = []
    for result in query_results:
        item = {
            "id": result[0],
            "name": result[1],
        }
        recipe_list.append(item)

    return recipe_list

def fetch_recipe_by_time(time) -> list:
    conn = db.connect()
    #SELECT name FROM Recipe WHERE recipe_id IN (SELECT recipe_id from Tags WHERE tag_name LIKE “”
    query_results = conn.execute("SELECT recipe_id, name FROM Recipe WHERE name LIKE '{} minute%%' LIMIT 20;".format(time)).fetchall()
    conn.close()
    print("recipe by time")
    recipe_list = []
    for result in query_results:
        item = {
            "id": result[0],
            "name": result[1],
        }
        recipe_list.append(item)

    return recipe_list

def fetch_recipe_by_num_ingr(num_ingr) -> list:
    conn = db.connect()
    #SELECT name FROM Recipe WHERE recipe_id IN (SELECT recipe_id from Tags WHERE tag_name LIKE “”
    query_results = conn.execute("SELECT recipe_id, name FROM Recipe WHERE name LIKE '{} ingredient%%' LIMIT 20;".format(num_ingr)).fetchall()
    conn.close()
    print("recipe by ingr")
    recipe_list = []
    for result in query_results:
        item = {
            "id": result[0],
            "name": result[1],
        }
        recipe_list.append(item)

    return recipe_list

def remove_list_by_id(list_id: int) ->None:
    conn = db.connect()
    query = 'Delete From PersonalizedList where id={};'.format(list_id)
    conn.execute(query)
    conn.close()

def create_list(name: str) -> None:
    conn = db.connect()
    query = 'Insert Into PersonalizedList (name) VALUES ("{}");'.format(name)
    conn.execute(query)
    # query_results = conn.execute("Select LAST_INSERT_ID();")
    # query_results = [x for x in query_results]
    # list_id = query_results[0][0]
    conn.close()

    # return list_id

def update_task_entry(task_id: int, text: str) -> None:
    """Updates task description based on given task_id

    Args:
        task_id (int): Targeted task_id
        text (str): Updated description

    Returns:
        None
    """

    conn = db.connect()
    query = 'Update tasks set task = "{}" where id = {};'.format(text, task_id)
    conn.execute(query)
    conn.close()


def update_status_entry(task_id: int, text: str) -> None:
    """Updates task status based on given task_id

    Args:
        task_id (int): Targeted task_id
        text (str): Updated status

    Returns:
        None
    """

    conn = db.connect()
    query = 'Update tasks set status = "{}" where id = {};'.format(text, task_id)
    conn.execute(query)
    conn.close()


def insert_new_task(text: str) ->  int:
    """Insert new task to todo table.

    Args:
        text (str): Task description

    Returns: The task ID for the inserted entry
    """

    conn = db.connect()
    query = 'Insert Into tasks (task, status) VALUES ("{}", "{}");'.format(
        text, "Todo")
    conn.execute(query)
    query_results = conn.execute("Select LAST_INSERT_ID();")
    query_results = [x for x in query_results]
    task_id = query_results[0][0]
    conn.close()

    return task_id


def remove_task_by_id(task_id: int) -> None:
    """ remove entries based on task ID """
    conn = db.connect()
    query = 'Delete From tasks where id={};'.format(task_id)
    conn.execute(query)
    conn.close()

def fetch_user(username: str, password: str):
    conn = db.connect()
    query = 'SELECT * FROM User WHERE username = {};'.format(
        username)
    
    query_results = conn.execute(query)
    conn.close()
    for result in query_results:
        print ("result 0: " + result[0] + "result 1: " + result[1] + "result 2: " + result[2] + "result 3: " + result[0] + "result 4: " + result[0])
        user_id = result[0]
        username = result[1]
        name = result[2]
        email = result[3]
        password = result[4]

    # User u(id, username, name, email, password)
    # return u
    return "getting user"

def fetch_recipe_by_name(name) -> list:
    conn = db.connect()
    query_results = conn.execute("SELECT recipe_id, name FROM Recipe WHERE name LIKE '%%{}%%';".format(name)).fetchall()

    conn.close()
    recipe_list = []
    for result in query_results:
        item = {
            "id": result[0],
            "name": result[1],
        }
        recipe_list.append(item)

    return recipe_list

def update_list_entry(old_name, new_name):
    conn = db.connect()
    query = 'UPDATE PersonalizedList SET name = "{}" where name = "{}";'.format(new_name, old_name)
    conn.execute(query)
    conn.close()
    return fetch_lists()

def add_user(username, name, email, password):
    conn = db.connect()
    query = 'Insert Into User (username, name, email, password) VALUES ("{}", "{}", "{}", "{}");'.format(
    username, name, email, password)
    conn.execute(query)
    conn.close()
    return fetch_users()

def delete_user(username):
    conn = db.connect()
    query = "DELETE FROM User WHERE username = '{}';".format(username)
    conn.execute(query)
    conn.close()
    return fetch_users()

def update_user_entry(old_name, new_name):
    conn = db.connect()
    query = 'UPDATE User SET username = "{}" where username = "{}";'.format(new_name, old_name)
    conn.execute(query)
    conn.close()
    return fetch_users()

def fetch_users():
    conn = db.connect()
    query_results = conn.execute("SELECT username FROM User;").fetchall()

    conn.close()
    list_name = []
    for result in query_results:
        item = {
            "username": result[0]
        }
        list_name.append(item)

    return list_name   

def add_list_by_name(list_name):
    conn = db.connect()
    query = 'Insert Into PersonalizedList (name, list_type) VALUES ("{}", "{}");'.format(
    list_name, int(0)) #type 0 means recipe
    conn.execute(query)
    conn.close()
    return fetch_lists()

def delete_list_by_name(list_name):
    conn = db.connect()
    query = "DELETE FROM PersonalizedList WHERE name LIKE '%%{}%%';".format(list_name) #type 0 means recipe
    conn.execute(query)
    conn.close()
    return fetch_lists()

def fetch_lists():
    conn = db.connect()
    query_results = conn.execute("SELECT list_id, name FROM PersonalizedList;").fetchall()

    conn.close()
    list_name = []
    for result in query_results:
        item = {
            "list_id": result[0],
            "name": result[1]
        }
        list_name.append(item)

    return list_name

def get_ingredient_name(ingredient_id):
    ret = None
    conn = db.connect()
    q1 = "SELECT ingredient_name FROM Ingredients WHERE ingredient_id = {};".format(ingredient_id)
    res = conn.execute(q1)
    for r in res:
        ret = r[0]
        return ret
    return ret

def add_ingredient_by_name(recipe_id, ingredient):  #TODO: fix tnis
    # global settings.min_ingredient_id
    conn = db.connect()
    q1 = "SELECT ingredient_id FROM Ingredients WHERE ingredient_name = '{}';".format(ingredient)
    res = conn.execute(q1)
    ing = 0
    for r in res:
        ing = r[0]
    # print(ing)
    
    if ing == 0:
        conn.execute("INSERT INTO Ingredients (ingredient_id, ingredient_name) VALUES ({}, '{}');".format(settings.min_ingredient_id, ingredient))
        ing = settings.min_ingredient_id
        settings.min_ingredient_id -= 1
        print(settings.min_ingredient_id)
    
    query = 'Insert Into RecipeHasIngredients (ingredient_id, recipe_id) VALUES ({}, {});'.format(
    ing, recipe_id) #type 0 means recipe
    conn.execute(query)
    conn.close()

def delete_ingredient(recipe_id, ingredient):
    conn = db.connect()
    q1 = "SELECT ingredient_id FROM Ingredients WHERE ingredient_name = '{}';".format(ingredient)
    res = conn.execute(q1)
    ing = 0
    for r in res:
        ing = r[0]
    query = "DELETE FROM RecipeHasIngredients where recipe_id = {} and ingredient_id = {};".format(recipe_id, ing) #type 0 means recipe
    conn.execute(query)
    conn.close()
    return fetch_lists()

def update_ingredient(recipe_id, ingredient_old, ingredient_new):
    # global min_ingredient_id
    conn = db.connect()
    q1 = "SELECT ingredient_id FROM Ingredients WHERE ingredient_name = '{}';".format(ingredient_old)
    res = conn.execute(q1)
    ing1 = 0
    for r in res:
        ing1 = r[0]
    if ing1 == 0:
        return
    q2 = "SELECT ingredient_id FROM Ingredients WHERE ingredient_name = '{}';".format(ingredient_new)
    r2 = conn.execute(q2)
    ing2 = 0
    for r in r2:
        ing2 = r[0]
    
    if ing2 == 0:
        conn.execute("INSERT INTO Ingredients (ingredient_id, ingredient_name) VALUES ({}, '{}');".format(settings.min_ingredient_id, ingredient_new))
        settings.min_ingredient_id -= 1
    
    query = 'UPDATE RecipeHasIngredients SET ingredient_id = {} where recipe_id = {} and ingredient_id = {};'.format(ing2, recipe_id, ing1)
    conn.execute(query)
    conn.close()
# def update_user(user_id, username, name, email, password):


def add_tag_by_name(recipe_id, tag_name):
    conn = db.connect()
    # q1 = "SELECT ingredient_id FROM Ingredients WHERE ingredient_name = '{}';".format(ingredient)
    # res = conn.execute(q1)
    # ing = 0
    # for r in res:
    #     ing = r[0]
    conn.execute(RecipeHasTags.__table__.insert().values(recipe_id=recipe_id, tag_name=tag_name))
    # query = 'Insert Into RecipeHasTags (recipe_id, tag_name) VALUES ({}, "{}");'.format(
    # recipe_id, tag_name) #type 0 means recipe
    # conn.execute(query)
    conn.close()

def delete_tag(recipe_id, tag_name):
    conn = db.connect()
    # q1 = "SELECT ingredient_id FROM Ingredients WHERE ingredient_name = '{}';".format(ingredient)
    # res = conn.execute(q1)
    # ing = 0
    # for r in res:
    #     ing = r[0]
    query = "DELETE FROM RecipeHasTags where recipe_id = {} and tag_name = '{}';".format(recipe_id, tag_name) #type 0 means recipe
    conn.execute(query)
    conn.close()
    return fetch_lists()

def update_tag(recipe_id, tag_old, tag_new):
    conn = db.connect()
    # q1 = "SELECT ingredient_id FROM Ingredients WHERE ingredient_name = '{}';".format(ingredient_old)
    # res = conn.execute(q1)
    # ing1 = 0
    # for r in res:
    #     ing1 = r[0]
    # q2 = "SELECT ingredient_id FROM Ingredients WHERE ingredient_name = '{}';".format(ingredient_new)
    # r2 = conn.execute(q2)
    # ing2 = 0
    # for r in r2:
    #     ing2 = r[0]
    # conn.execute(RecipeHasTags.__table__.update().values(recipe_id=recipe_id, tag_name=tag_name))

    query = 'UPDATE RecipeHasTags SET tag_name = "{}" where recipe_id = {} and tag_name = "{}";'.format(tag_new, recipe_id, tag_old)
    conn.execute(query)
    conn.close()
# def remove_user(user_id):

def add_recipe_by_id(id, recipe_id):
    conn = db.connect()
    query = 'Insert Into PersonalizedListContainsRecipes (recipe_id, list_id) VALUES ("{}", "{}");'.format(
    recipe_id, id) #type 0 means recipe
    conn.execute(query)
    conn.close()
    return fetch_list_recipes(id)

def delete_recipe_by_id(id, recipe_id):
    conn = db.connect()
    query = "DELETE FROM PersonalizedListContainsRecipes WHERE list_id = {} AND recipe_id = {};".format(id, recipe_id) #type 0 means recipe
    conn.execute(query)
    conn.close()
    return fetch_list_recipes(id)

def fetch_list_recipes(id):
    conn = db.connect()
    query = "SELECT recipe_id, name FROM PersonalizedListContainsRecipes NATURAL JOIN Recipe WHERE list_id = {};".format(id)
    query_results = conn.execute(query).fetchall()

    conn.close()
    list_name = []
    for result in query_results:
        item = {
            "id": result[0],
            "name":result[1]
        }
        list_name.append(item)

    return list_name

def fetch_list_name_from_id(id):
    conn = db.connect()
    query = "SELECT name FROM PersonalizedList WHERE list_id = {};".format(id)
    query_results = conn.execute(query).fetchall()
    print(query_results)
    conn.close()
    # list_name = []
    # for result in query_results:
    #     item = {
    #         "name":result[0]
    #     }
    #     list_name.append(item)

    return query_results[0][0]


class User:
    def __init__(self, user_id, username, name, email, password):
        self.user_id = user_id
        self.username = username
        self.name = name
        self.email = email
        self.password = password

class Recipe:
    def __init__(self, id, minutes, num_steps, recipe_steps, contributor_id, name, sugar, sodium, protein, total_fat, saturated_fat, calories, carbs, ingredients, tags):
        self.id = id
        self.minutes = minutes 
        self.num_steps = num_steps
        self.recipe_steps = recipe_steps 
        self.contributor_id = contributor_id 
        self.name = name 
        self.sugar = sugar
        self.sodium = sodium
        self.protein = protein 
        self.total_fat = total_fat
        self.saturated_fat = saturated_fat 
        self.calories = calories
        self.carbs = carbs
        self.ingredients = ingredients
        self.tags = tags

    def __str__(self): 
        return "This is the recipe: {},\n minutes: {},\n number of steps: {},\n recipe steps: {},\n contributor id:\n {}, name:\n {}, sugar:\n {}, sodium:\n {}, protein:\n {}, total_fat:\n {}, saturated_fat:\n {}, calories:\n {}, carbs:\n {}, ingredients:\n {}, tags:\n {}".format(self.id, self.minutes, self.num_steps, self.recipe_steps, self.contributor_id, self.name, self.sugar, self.sodium, self.protein, self.total_fat, self.saturated_fat, self.calories, self.carbs, self.ingredients, self.tags)




# other_db = SQLAlchemy()

# # tsvector type declaration
# class tsvector(types.TypeDecorator):
#     impl = types.UnicodeText

# @compiles(tsvector, 'postgresql')
# def compile_tsvector(element, compiler, **kw):
#     return 'tsvector'

# table declaration
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from app import base

class RecipeHasTags(base):
    __tablename__ = "RecipeHasTags"
    recipe_id = Column(Integer, primary_key=True)
    tag_name = Column(String, primary_key=True)

# custom trigger DDL
rht_insert_trig = DDL('''\
    CREATE TRIGGER TagTrig BEFORE INSERT OR UPDATE
    ON RecipeHasTags
    FOR EACH ROW 
        BEGIN
            SET @name = (SELECT tag_name FROM Tags
                                WHERE tag_name = new.tag_name)
            IF @name IS NULL THEN
                INSERT INTO Tags(tag_name)
                VALUES(new.tag_name)
        END;
    ''')

# # event listener to trigger on data insert to MyTable
event.listen(RecipeHasTags, 'before_insert', rht_insert_trig)