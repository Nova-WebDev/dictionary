import time
import sqlite3
from db.role import RoleRepository
from logic.actions import DictionaryActions, UserActions, BlockActions, TokenValidator

def main_menu_flow(cursor, token):
    role_repo = RoleRepository(cursor)
    dict_actions = DictionaryActions(cursor)
    user_actions = UserActions(cursor)
    block_actions = BlockActions(cursor)

    menu_normal_user = """
1) Show dict
2) Translate from English to Farsi
3) Translate from Farsi to English
9) Log out
0) Exit the program
"""

    menu_power_user = """
1) Show dict
2) Translate from English to Farsi
3) Translate from Farsi to English
4) Add a new word
5) Edit an existing word
6) Delete a word
9) Log out
0) Exit the program
"""

    menu_admin_user = """
1) Show dict
2) Translate from English to Farsi
3) Translate from Farsi to English
4) Add a new word
5) Edit an existing word
6) Delete a word
11) Show users
12) Create a new user
13) Change authorization
14) Show blocked users
15) Block user
16) Unblock user
9) Log out
0) Exit the program
"""

    while True:
        time.sleep(2)

        if not TokenValidator.is_token_valid(token):
            print("Session expired. Please log in again.")
            return True

        payload = TokenValidator.extract_payload(token)
        role = payload["role"]
        username = payload["sub"]

        if role == "normal_user":
            print(menu_normal_user)
        elif role == "power_user":
            print(menu_power_user)
        elif role == "admin":
            print(menu_admin_user)

        choice = input("Enter your choice: ").strip()

        if choice == "0":
            return False

        elif choice == "9":
            print("Logging out...")
            return True

        elif choice == "1":
            dict_actions.print_all_dictionary_words(token=token)

        elif choice == "2":
            en_word = input("Enter English word: ").strip()
            dict_actions.show_fa_translations(en_word, token=token)

        elif choice == "3":
            fa_word = input("Enter Persian word: ").strip()
            dict_actions.show_en_translations(fa_word, token=token)

        elif choice == "4":
            en_word = input("Enter English word: ").strip()
            fa_word = input("Enter Persian translation: ").strip()
            try:
                dict_actions.add_new_word(en_word, fa_word, author_username=username, token=token)
            except sqlite3.IntegrityError:
                print("Duplicate value en-word and fa-word!")

        elif choice == "5":
            dict_actions.print_all_dictionary_words(token=token)
            try:
                word_id = int(input("Enter word ID to edit: ").strip())
            except ValueError:
                print("Invalid word ID format.")
                continue
            new_en = input("Enter new English word: ").strip()
            new_fa = input("Enter new Persian word: ").strip()

            if role == "admin":
                dict_actions.edit_any_word(word_id, new_en, new_fa, token=token)
            else:
                dict_actions.edit_own_word(word_id, new_en, new_fa, author_username=username, token=token)

        elif choice == "6":
            dict_actions.print_all_dictionary_words(token=token)
            try:
                word_id = int(input("Enter word ID to delete: ").strip())
            except ValueError:
                print("Invalid word ID format.")
                continue
            if role == "admin":
                dict_actions.delete_any_word(word_id, token=token)
            else:
                dict_actions.delete_own_word(word_id, author_username=username, token=token)

        elif choice == "11":
            user_actions.show_all_users(current_username=username, token=token)

        elif choice == "12":
            new_username = input("Enter new username: ").strip()
            new_email = input("Enter new email: ").strip()
            new_password = input("Enter new password: ").strip()

            roles = role_repo.get_all_roles()
            print("Available roles:")
            for role_obj in roles:
                print(f"{role_obj['id']}) {role_obj['role_name']}")

            try:
                role_id = int(input("Enter role ID: ").strip())
            except ValueError:
                print("Invalid role ID format.")
                continue

            selected_role = next((r for r in roles if r["id"] == role_id), None)
            if not selected_role:
                print("Role ID not found.")
                continue

            confirm = False
            if selected_role["role_name"] == "admin":
                confirm = input("Type 'ok' to confirm admin downgrade if needed: ").strip().lower() == "ok"

            user_actions.create_new_user(new_username, new_email, new_password, role_id,
                                         current_admin_username=username,
                                         confirm_admin_downgrade=confirm,
                                         token=token)

        elif choice == "13":
            user_actions.show_all_users(current_username=username, token=token)

            try:
                target_id = int(input("Enter user ID to change role: ").strip())
            except ValueError:
                print("Invalid user ID format.")
                continue

            roles = role_repo.get_all_roles()
            print("Available roles:")
            for role_obj in roles:
                print(f"{role_obj['id']}) {role_obj['role_name']}")

            try:
                role_id = int(input("Enter new role ID: ").strip())
            except ValueError:
                print("Invalid role ID format.")
                continue

            selected_role = next((r for r in roles if r["id"] == role_id), None)
            if not selected_role:
                print("Role ID not found.")
                continue

            confirm = False
            if selected_role["role_name"] == "admin":
                confirm = input("Type 'ok' to confirm admin downgrade if needed: ").strip().lower() == "ok"

            user_actions.change_user_role(target_user_id=target_id, new_role_id=role_id,
                                          current_admin_username=username,
                                          confirm_admin_downgrade=confirm,
                                          token=token)

        elif choice == "14":
            block_actions.show_blocked_users(token=token)

        elif choice == "15":
            block_actions.show_unblocked_users(current_admin_username=username, token=token)
            try:
                target_id = int(input("Enter user ID to block: ").strip())
            except ValueError:
                print("Invalid user ID format.")
                continue
            block_actions.block_user_by_id(target_user_id=target_id,
                                           current_admin_username=username,
                                           token=token)

        elif choice == "16":
            block_actions.show_users_to_unblock(current_admin_username=username, token=token)
            try:
                target_id = int(input("Enter user ID to unblock: ").strip())
            except ValueError:
                print("Invalid user ID format.")
                continue
            block_actions.unblock_user_by_id(target_user_id=target_id,
                                             current_admin_username=username,
                                             token=token)

        else:
            print("Invalid choice. Please try again.")
