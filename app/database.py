"""Defines all the functions related to the database"""
from app import db
from sqlalchemy.sql import func
# from flask_sqlalchemy import SQLAlchemy

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
    query_results = conn.execute("(SELECT r.name, COUNT(ingredient_id) as num_ingredients " +
                                "FROM RecipeHasIngredients rhi natural join Recipe r " +
                                "WHERE r.name LIKE '5 minute%%' AND rhi.recipe_id IN (SELECT recipe_id FROM Review GROUP BY recipe_id HAVING avg(rating) > 3) " +
                                "GROUP BY r.name " +
                                "HAVING num_ingredients < 8 " +
                                "ORDER BY num_ingredients ASC, r.name ASC) LIMIT 15;").fetchall()
    #print("query results: " + query_results)
    conn.close()
    recipes = []
    for result in query_results:
        #print("result: " + result)
        item = {
            "id": result[1],
            "name": result[0]
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
    print(query_results)
    conn.close()
    recipe_list = []
    # for result in query_results:
    #     item = {
    #         "id": result[0],
    #         "name": result[5],
    #         # "status": result[2]
    #     }
    #     recipe_list.append(item)
    # print(recipe_list)
    return recipe_list
    
def fetch_healthy() -> list:
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute("(SELECT r.recipe_id, r.name, r.calories as Calories " +
                                "FROM Recipe r JOIN RecipeHasTags rt ON r.recipe_id = rt.recipe_id " + 
                                "WHERE rt.tag_name = 'healthy' OR rt.tag_name = 'very-low-carbs' AND r.recipe_id IN (SELECT recipe_id FROM Review GROUP BY recipe_id HAVING COUNT(rating) > 4) " +
                                "GROUP BY r.recipe_id) " + 
                                "UNION " + 
                                "(SELECT r.recipe_id, r.name, r.calories as Calories " +
                                "FROM Recipe r JOIN RecipeHasTags rt ON r.recipe_id = rt.recipe_id " +
                                "WHERE r.sugar < 50 AND rt.tag_name = 'desserts' AND r.recipe_id IN (SELECT recipe_id FROM Review GROUP BY recipe_id HAVING AVG(rating) > 2)) LIMIT 15;").fetchall()
    #print(query_results)
    conn.close()
    recipe_list = []
    for result in query_results:
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

def fetch_personal_lists() -> list:
    conn = db.connect()
    query_results = conn.execute("SELECT * FROM PersonalizedList;").fetchall()

    conn.close()
    recipe_list = []
    for result in query_results:
        item = {
            "id": result[0],
            "name": result[1],
            "date_created": result[2]
        }
        recipe_list.append(item)

    return recipe_list

def update_list_entry(list_id: int, new_name: str) -> None:
    conn = db.connect()
    query = 'UPDATE PersonalizedList SET name = "{}" where list_id = {};'.format(new_name, list_id)
    conn.execute(query)
    conn.close()

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
    query_results = conn.execute("SELECT * FROM Recipe WHERE name LIKE '%%name%%';").fetchall()

    conn.close()
    recipe_list = []
    for result in query_results:
        item = {
            "id": result[0],
            "name": result[1],
        }
        recipe_list.append(item)

    return recipe_list

def add_user(user_id, username, name, email, password):
    conn = db.connect()
    query = 'Insert Into User (id, username, name, email, password) VALUES ("{}", "{}", "{}", "{}", "{}");'.format(
    user_id, username, name, email, password)
    conn.execute(query)
    conn.close()


# def update_user(user_id, username, name, email, password):


# def remove_user(user_id):


class User:
    def __init__(self, user_id, username, name, email, password):
        self.user_id = user_id
        self.username = username
        self.name = name
        self.email = email
        self.password = password
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String, Float, Text
# class Recipe(other_db.Model):
#     __tablename__ = "Recipe"
#     id = Column(Integer, primary_key = True)
#     minutes = Column(Integer)
#     num_steps = Column(Integer)
#     recipe_steps = Column(Text)
#     contributor_id = Column(Integer)
#     name = Column(String)
#     sugar = Column(Float)
#     sodium = Column(Float)
#     protein = Column(Float)
#     total_fat = Column(Float)
#     saturated_fat = Column(Float)
#     calories = Column(Float)
#     carbs = Column(Text)
