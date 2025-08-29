import pprint, random, time, smtplib
from setting import TOKEN_EXPIRATION
from email.mime.text import MIMEText
from data_layer import check_password, is_valid_email, get_blocked_users, get_user, update_user, insert_user, \
    find_user_by_email, get_dictionary


def show_blocked_users():
    blocked = get_blocked_users()
    if blocked:
        print("Blocked users:")
        for u in blocked:
            print(u)
    else:
        print("No blocked users.")


def unblock_user(username):
    my_user = get_user(username)
    if not my_user:
        print("User not found.")
        return False

    password = my_user["password"]
    if not password.startswith("!:"):
        print("User is not blocked.")
        return False

    # حذف پیشوند "!:" برای آن‌بلاک کردن
    my_user["password"] = password[2:]

    update_user(username, my_user["mail"], my_user["password"], my_user["authorization"], flag=False)
    return True



def block_user(username):
    my_user = get_user(username)
    if not my_user:
        print("User not found.")
        return False

    password = my_user["password"]
    if password.startswith("!:"):
        print("User is already blocked.")
        return False

    my_user["password"] = f"!:{password}"

    update_user(username, my_user["mail"], my_user["password"], my_user["authorization"], flag=False)
    return True

############
def login_user():
    username = input("username: ").strip()
    password = input("password: ").strip()

    user_data = get_user(username)
    if not user_data:
        print("Username not found. Please sign up first.")
        return {}

    if not check_password(password, user_data["password"]):
        print("Incorrect password. Please try again.")
        return {}

    token = f"{username}_{random.randrange(0, 20)}"
    created_at = time.time()

    print(f"Welcome, {username}. Your token is: {token}")

    return {
        token: {
            "username": username,
            "authorization": user_data["authorization"],
            "created_at": created_at
        }
    }


def sign_in_user():
    username = input("username: ").strip()
    mail = input("email address: ").strip()
    password = input("password").strip()

    user_data = get_user(username)
    if user_data:
        print("This username is already taken. Please choose another one.")
        return {}

    if not is_valid_email(mail):
        print("Invalid email format.")
        return {}

    success = insert_user(username, mail, password)
    if not success:
        print("Failed to create user.")
        return {}

    token = f"{username}_{random.randrange(0, 20)}"
    created_at = time.time()

    print(f"Sign up successful. Welcome, {username}. Your token is: {token}")

    return {
        token: {
            "username": username,
            "authorization": "normal_user",
            "created_at": created_at
        }
    }


def send_recovery_code(email, users_dict):
    sender_email = "sudo.novawebdev@gmail.com"
    app_password = "gwyttbuawygrvjxu"

    username = None
    for u, info in users_dict.items():
        if info["mail"] == email:
            username = u
            break

    if not username:
        print("Email not found.")
        return None

    code = str(random.randrange(1000, 10000))

    message = MIMEText(f"Hi {username}!\nYour recovery code: {code}")
    message["Subject"] = "Password Reset Code"
    message["From"] = sender_email
    message["To"] = email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.send_message(message)
        print("Recovery code sent.")
        return {"username": username, "code": code}
    except Exception as e:
        print(f"Failed to send email: {e}")
        return None


def reset_password():
    email = input("What's your email address: ").strip()

    user_info = find_user_by_email(email)
    if not user_info:
        print("Email not found.")
        return {}

    result = send_recovery_code(email, user_info)
    if not result:
        return {}

    entered = input("Recovery code: ").strip()
    if entered != result["code"]:
        print("Invalid code.")
        return {}

    new_pass = input("Create a new password: ").strip()
    success = update_user(
        username=result["username"],
        mail=user_info["info"]["mail"],
        password=new_pass,
        authorization=user_info["info"]["authorization"]
    )

    if success:
        print("Password reset successful.")
        return {
            "username": result["username"],
            "authorization": user_info["info"]["authorization"],
            "updated_at": time.time()
        }
    else:
        print("Failed to update password.")
        return {}


def print_dictionary():
    pprint.pprint(get_dictionary())


def is_token_valid(token, active_users):
    if token not in active_users:
        return False

    created_at = active_users[token]["created_at"]
    now = time.time()

    if now - created_at > TOKEN_EXPIRATION:
        del active_users[token]
        return False

    return True
