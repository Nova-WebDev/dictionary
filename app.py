from bussiness_layer import is_token_valid, print_dictionary, block_user, unblock_user, show_blocked_users, login_user, \
    sign_in_user, reset_password
from data_layer import get_translation, find_key_by_translation, insert_translation, update_translation, \
    delete_translation, get_user, update_user, insert_user

active_users = {}


def main_menu_flow(your_token):
    menu_normal_user = """
1) Translate from English to Farsi
2) Translate from Farsi to English
8) Show dict
9) Log out
0) Exit the program
"""
    menu_power_user = """
1) Translate from English to Farsi
2) Translate from Farsi to English
3) Edit an existing word
4) Add a new word
5) Delete a word
8) Show dict
9) Log out
0) Exit the program
"""
    menu_admin_user = """
1) Translate from English to Farsi
2) Translate from Farsi to English
3) Edit an existing word
4) Add a new word
5) Delete a word
6) Change authorization
7) Create a new user
10) Block user
11) Unblock user
12) Show blocked users
8) Show dict
9) Log out
0) Exit the program
"""

    while is_token_valid(your_token, active_users):
        current_user = active_users[your_token]
        role = current_user["authorization"]

        if role == "admin":
            print(menu_admin_user)
        elif role == "power_user":
            print(menu_power_user)
        else:
            print(menu_normal_user)

        action = input("\nPlease select an option: ").strip()

        if action == "0":
            print("Exiting the program. Goodbye.")
            del active_users[your_token]
            return False

        elif action == "9":
            print("Logged out successfully.")
            del active_users[your_token]
            return True

        elif action == "1":
            word = input("Enter English word: ").lower().strip()
            result = get_translation(word)
            if result:
                print(f"{word}: {result}")
            else:
                print(f"'{word}' not found.")

        elif action == "2":
            word = input("Enter Farsi word: ").strip()
            result = find_key_by_translation(word)
            if result:
                print(f"{word}: {result}")
            else:
                print(f"'{word}' not found.")

        elif action == "3":
            if role in ["power_user", "admin"]:
                print_dictionary()
                word = input("Word to edit: ").lower().strip()
                new = input("New translation: ")
                if update_translation(word, new):
                    print("Translation updated.")
                else:
                    print("Update failed.")
            else:
                print("Access denied.")

        elif action == "4":
            if role in ["power_user", "admin"]:
                word = input("New English word: ").lower().strip()
                fa = input("Farsi translation: ")
                if insert_translation(word, fa):
                    print("Word added.")
                else:
                    print("Word already exists.")
            else:
                print("Access denied.")

        elif action == "5":
            if role in ("power_user", "admin"):
                word = input("Word to delete: ").lower().strip()
                if delete_translation(word):
                    print("Word deleted.")
                else:
                    print("Word not found.")
            else:
                print("Access denied.")

        elif action == "6":
            if role == "admin":
                uname = input("Username to change role: ").strip()
                user = get_user(uname)
                if not user or uname == current_user["username"]:
                    print("Invalid username.")
                    continue

                print(f"Current role: {user['authorization']}")
                new_auth = input("New role (1=normal, 2=power, 3=admin, 0=cancel): ").strip()

                if new_auth == "0":
                    print("Canceled.")
                    continue

                roles = {"1": "normal_user", "2": "power_user", "3": "admin"}
                if new_auth not in roles:
                    print("Invalid selection.")
                    continue

                if new_auth == "3":
                    sure = input("This will downgrade your access. Continue? (1 = Yes): ").strip()
                    if sure != "1":
                        print("Canceled.")
                        continue
                    update_user(current_user["username"], current_user["mail"],
                                get_user(current_user["username"])["password"], "power_user")
                    current_user["authorization"] = "power_user"

                update_user(uname, user["mail"], user["password"], roles[new_auth])
                print(f"{uname}'s role updated to {roles[new_auth]}.")
            else:
                print("Access denied.")

        elif action == "7":
            if role == "admin":
                uname = input("New username: ").strip()
                mail = input("Email: ").strip()
                password = input("Password: ").strip()
                role_input = input("Role (1=normal, 2=power, 3=admin, 0=cancel): ").strip()

                if role_input == "0":
                    print("Canceled.")
                    continue

                roles = {"1": "normal_user", "2": "power_user", "3": "admin"}
                if role_input not in roles:
                    print("Invalid selection.")
                    continue

                if get_user(uname):
                    print("Username already exists.")
                    continue

                if role_input == "3":
                    sure = input("This will downgrade your access. Continue? (1 = Yes): ").strip()
                    if sure != "1":
                        print("Canceled.")
                        continue
                    update_user(current_user["username"], current_user["mail"],
                                get_user(current_user["username"])["password"], "power_user")
                    current_user["authorization"] = "power_user"

                insert_user(uname, mail, password, roles[role_input])
                print(f"User '{uname}' created with role {roles[role_input]}.")
            else:
                print("Access denied.")

        elif action == "10":
            if role == "admin":
                uname = input("Username to block: ").strip()
                if block_user(uname):
                    print("User blocked.")
                else:
                    print("Blocking failed.")
            else:
                print("Access denied.")

        elif action == "11":
            if role == "admin":
                uname = input("Username to unblock: ").strip()
                if unblock_user(uname):
                    print("User unblocked.")
                else:
                    print("Unblocking failed.")
            else:
                print("Access denied.")

        elif action == "12":
            if role == "admin":
                show_blocked_users()
            else:
                print("Access denied.")

        elif action == "8":
            print_dictionary()

        else:
            print("Invalid selection.")

    return True


def register_flow():
    register_menu = """
1) Log in
2) Sign up
3) Forgot password
0) Exit
"""
    my_token = None

    while my_token is None:
        register_value = input(register_menu + "\nPlease select an option: ").strip()

        if register_value == "0":
            print("Exiting the program. Goodbye.")
            return False, None

        elif register_value == "1":
            session = login_user()
            if session:
                active_users.update(session)
                my_token = list(session.keys())[0]
                print("Login successful.")

        elif register_value == "2":
            session = sign_in_user()
            if session:
                active_users.update(session)
                my_token = list(session.keys())[0]
                print("Sign up successful.")

        elif register_value == "3":
            result = reset_password()
            if result:
                print("You can now log in with your new password.")

        else:
            print("Invalid input. Please enter a valid option.")

    return True, my_token


def run_program():
    while True:
        success, your_token = register_flow()
        if not success:
            break

        result = main_menu_flow(your_token)
        if not result:
            break


if __name__ == "__main__":
    run_program()
