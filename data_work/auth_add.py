import json
import os

def load_users_data():
    if not os.path.exists("data/user.json"):
        return []
    with open ('data/user.json', 'r') as f:
        return json.load(f)

def check_credentials(username=None, password=None):
    users_information = load_users_data()

    for user in users_information:
        if user["username"] == username and user["password"] == password:
            print("Login successful!")
            return user["role"]

    return None

def add_user_to_json(username, password, role="member"):
    if not os.path.exists("data/user.json"):
        return []
    with open ('data/user.json', 'r') as f:
        users = json.load(f)  

    users.append({"username": username, "password": password, "role": role})

    with open ('data/user.json', "w",) as f:
        json.dump(users, f, indent=4)