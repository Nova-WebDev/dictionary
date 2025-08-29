import json, bcrypt

def is_valid_email(email):
    if email.count("@") != 1:
        return False

    at_index = email.index("@")
    if "." not in email[at_index + 1:]:
        return False

    return True


def hash_password(password, rounds=4):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds))
    return hashed.decode()


def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())





def get_blocked_users():
    try:
        with open("users.json", "r", encoding="utf-8") as f:
            users = json.load(f)
        if not isinstance(users, dict):
            print("Invalid user data format.")
            return
    except Exception as e:
        print(f"User data not found: {e}")
        return

    return [u for u, info in users.items() if isinstance(info, dict) and info.get("password", "").startswith("!:")]


def get_user(username, file_path="users.json"):
    try:
        with open(file_path, "r") as f:
            users = json.load(f)
        return users.get(username)
    except Exception as e:
        print(f"Error from get user: {e}")
        return None


def find_user_by_email(email, file_path="users.json"):
    try:
        with open(file_path, "r") as f:
            users = json.load(f)
        for username, info in users.items():
            if info["mail"] == email:
                return {"username": username, "info": info}
        return {}
    except Exception as e:
        print(f"Error reading user data: {e}")
        return {}


def update_user(username, mail, password, authorization="normal_user", file_path="users.json", flag=True):
    if not is_valid_email(mail):
        print("Invalid email format.")
        return False

    try:
        with open(file_path, "r") as f:
            users = json.load(f)
    except Exception as e:
        print(f"Error reading file in update_user: {e}")
        return False

    if username not in users:
        print("Username not found.")
        return False

    users[username] = {
        "mail": mail,
        "password": hash_password(password) if flag else password,
        "authorization": authorization
    }

    try:
        with open(file_path, "w") as f:
            json.dump(users, f, indent=4)
        return True
    except Exception as e:
        print(f"Error writing file in update_user: {e}")
        return False


def insert_user(username, mail, password, authorization="normal_user", file_path="users.json"):
    if not is_valid_email(mail):
        print("Invalid email format.")
        return False

    try:
        with open(file_path, "r") as f:
            users = json.load(f)
    except Exception as e:
        print(f"Error reading file in insert_user: {e}")
        users = {}

    if username in users:
        print("Username already exists.")
        return False

    users[username] = {
        "mail": mail,
        "password": hash_password(password),
        "authorization": authorization
    }

    try:
        with open(file_path, "w") as f:
            json.dump(users, f, indent=4)
        return True
    except Exception as e:
        print(f"Error writing file in insert_user: {e}")
        return False






def get_translation(en_word, file_path="dictionary.json"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get(en_word, None)
    except Exception as e:
        print(f"Error reading dictionary: {e}")
        return None


def delete_translation(en_word, file_path="dictionary.json"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Dictionary not found: {e}")
        return False

    if en_word not in data:
        print("Word not found.")
        return False

    del data[en_word]

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Error deleting word: {e}")
        return False


def find_key_by_translation(fa_word, file_path="dictionary.json"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for key, value in data.items():
            if value == fa_word:
                return key
        return None
    except Exception as e:
        print(f"Error reading dictionary: {e}")
        return None


def insert_translation(en_word, fa_word, file_path="dictionary.json"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error from find by key: {e}")
        data = {}

    if en_word in data:
        return False

    data[en_word] = fa_word

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Error saving dictionary: {e}")
        return False


def update_translation(en_word, new_fa_word, file_path="dictionary.json"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Dictionary not found: {e}")
        return False

    if en_word not in data:
        print("Word not found.")
        return False

    data[en_word] = new_fa_word

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Error updating dictionary: {e}")
        return False


def get_dictionary(file_path="dictionary.json"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return  data
    except Exception as e:
        print(f"Error printing dictionary: {e}")
        return  None

