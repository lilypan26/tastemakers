

def init_min_ing_id():
  global min_ingredient_id
  min_ingredient_id = -1
  with open('app\secret_file.txt', 'r') as f:
    for line in f:
      min_ingredient_id = int(line)
      print(min_ingredient_id)

def save_min_ingredient_id():
    # global min_ingredient_id
    print("end " + str(min_ingredient_id))
    f = open('app\secret_file.txt', 'w')
    f.write(str(min_ingredient_id))
    f.close()