from db.word_db import db_get_all_words_with_authors, db_english_word_exists, db_get_fa_translations_by_en_word, \
    db_persian_word_exists, db_get_en_translations_by_fa_word, db_insert_word, \
    db_word_id_belongs_to_author, db_update_word_by_id, db_word_id_exists, \
    db_author_has_words, db_delete_word_by_id
from db.user_db import get_all_users, user_exists, email_exists, insert_user, get_user_id_by_username, \
    update_user_by_id, db_get_all_blocked_users, db_unblock_user_by_id, is_user_blocked, db_block_user_by_id
from db.role import role_id_exists, get_role_name_by_id

from setting import MAX_WORD_LENGTH, BCRYPT_SALT_ROUNDS, PUBLIC_KEY_PATH
import bcrypt, json, time
from cryptography.hazmat.primitives import serialization

from cryptography.exceptions import InvalidSignature


def is_token_valid(token):
    if not isinstance(token, str) or not token.strip():
        return False

    try:
        payload_json, signature_hex = token.rsplit(".", 1)
        signature_bytes = bytes.fromhex(signature_hex)

        with open(PUBLIC_KEY_PATH, "rb") as f:
            public_key = serialization.load_pem_public_key(f.read())

        public_key.verify(signature_bytes, payload_json.encode("utf-8"))

        payload = json.loads(payload_json)
        exp = payload.get("exp")
        if not isinstance(exp, int) or int(time.time()) > exp:
            return False

        return True

    except (ValueError, InvalidSignature, json.JSONDecodeError, FileNotFoundError):
        return False

def extract_payload(token):
    if not is_token_valid(token):
        return None

    try:
        payload_json = token.rsplit(".", 1)[0]
        return json.loads(payload_json)
    except (ValueError, json.JSONDecodeError):
        return None

def access_control(func):
    def wrapper(*args, **kwargs):
        token = kwargs.pop("token", None)
        allowed_roles = kwargs.pop("allowed_roles", ())

        if not isinstance(token, str) or not token.strip():
            return None
        if not allowed_roles:
            return None
        if not is_token_valid(token):
            return None

        payload = extract_payload(token)
        if not payload or payload.get("role") not in allowed_roles:
            return None

        return func(*args, **kwargs)
    return wrapper

@access_control
def show_fa_translations(en_word):
    if not db_english_word_exists(en_word):
        print("Word not found in dictionary.")
        return

    translations = db_get_fa_translations_by_en_word(en_word)
    for fa_word, author in translations.items():
        print(f"{fa_word}     =>    {author}")

@access_control
def show_en_translations(fa_word):
    if not db_persian_word_exists(fa_word):
        print("Word not found in dictionary.")
        return

    translations = db_get_en_translations_by_fa_word(fa_word)
    for en_word, author in translations.items():
        print(f"{en_word} => {author}")

@access_control
def print_all_dictionary_words():
    words = db_get_all_words_with_authors()
    if not words:
        print("Dictionary is empty.")
        return

    print("All dictionary entries:")
    for entry in words:
        print(f"{entry['id']}) {entry['english_word']} = {entry['persian_word']}     =>    {entry['author']}")


@access_control
def add_new_word(en_word, fa_word, author_username):
    if len(en_word) > MAX_WORD_LENGTH or len(fa_word) > MAX_WORD_LENGTH:
        print(f"Each word must be at most {MAX_WORD_LENGTH} characters.")
        return

    # if db_translation_pair_exists(en_word, fa_word):
    #     print("This translation pair already exists.")
    #     return

    db_insert_word(en_word, fa_word, author_username)
    print("Word added successfully.")


@access_control
def edit_own_word(word_id, new_en, new_fa, author_username):
    if not db_author_has_words(author_username):
        print("You haven't submitted any words yet.")
        return

    if not db_word_id_belongs_to_author(word_id, author_username):
        print("You are not allowed to edit this word.")
        return

    if len(new_en) > MAX_WORD_LENGTH or len(new_fa) > MAX_WORD_LENGTH:
        print(f"Each word must be at most {MAX_WORD_LENGTH} characters.")
        return

    db_update_word_by_id(word_id, {
        "english_word": new_en,
        "persian_word": new_fa
    })

    print("Word updated successfully.")


@access_control
def edit_any_word(word_id, new_en, new_fa):
    if not db_word_id_exists(word_id):
        print("Word ID not found.")
        return

    if len(new_en) > MAX_WORD_LENGTH or len(new_fa) > MAX_WORD_LENGTH:
        print(f"Each word must be at most {MAX_WORD_LENGTH} characters.")
        return

    db_update_word_by_id(word_id, {
        "english_word": new_en,
        "persian_word": new_fa
    })

    print("Word updated successfully.")


@access_control
def delete_own_word(word_id, author_username):
    if not db_author_has_words(author_username):
        print("You haven't submitted any words yet.")
        return

    if not db_word_id_belongs_to_author(word_id, author_username):
        print("You are not allowed to delete this word.")
        return

    db_delete_word_by_id(word_id)
    print("Word deleted successfully.")

@access_control
def delete_any_word(word_id):
    if not db_word_id_exists(word_id):
        print("Word ID not found.")
        return

    db_delete_word_by_id(word_id)
    print("Word deleted successfully.")

@access_control
def show_all_users(current_username):
    users = get_all_users()

    print("All users (excluding yourself):")
    for user_id, data in users.items():
        if data["username"] == current_username:
            continue
        print(f"{user_id}) {data['username']} | {data['email']} | {data['role']}")

@access_control
def create_new_user(new_username, new_email, new_password, role_id, current_admin_username, confirm_admin_downgrade=False):
    if user_exists(new_username):
        print("Username already exists.")
        return

    if email_exists(new_email):
        print("Email already exists.")
        return

    hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt(BCRYPT_SALT_ROUNDS))

    if not role_id_exists(role_id):
        print("Role ID not found.")
        return

    selected_role_name = get_role_name_by_id(role_id)

    if selected_role_name == "admin":
        if not confirm_admin_downgrade:
            print("Operation cancelled. Admin downgrade not confirmed.")
            return

        insert_user(new_username, new_email, hashed_password, "admin")
        current_admin_id = get_user_id_by_username(current_admin_username)
        update_user_by_id(current_admin_id, {"role_name": "power_user"})

        print("User created as admin. Your role has been downgraded to power_user.")
        return

    insert_user(new_username, new_email, hashed_password, selected_role_name)
    print(f"User created successfully with role '{selected_role_name}'.")

@access_control
def change_user_role(target_user_id, new_role_id, current_admin_username, confirm_admin_downgrade=False):
    users = get_all_users()
    if target_user_id not in users or users[target_user_id]["username"] == current_admin_username:
        print("Invalid user ID. You cannot change your own role or select a non-existent user.")
        return

    if not role_id_exists(new_role_id):
        print("Role ID not found.")
        return

    selected_role_name = get_role_name_by_id(new_role_id)

    if selected_role_name == "admin":
        if not confirm_admin_downgrade:
            print("Operation cancelled. Admin downgrade not confirmed.")
            return

        update_user_by_id(target_user_id, {"role_name": "admin"})
        current_admin_id = get_user_id_by_username(current_admin_username)
        update_user_by_id(current_admin_id, {"role_name": "power_user"})

        print("Role updated. You are now a power_user.")
        return

    update_user_by_id(target_user_id, {"role_name": selected_role_name})
    print(f"Role updated successfully to '{selected_role_name}'.")

@access_control
def show_blocked_users():
    blocked_users = db_get_all_blocked_users()
    if not blocked_users:
        print("No blocked users found.")
        return

    print("Blocked users:")
    for user_id, username in blocked_users.items():
        print(f"{user_id}) {username}")


@access_control
def show_unblocked_users(current_admin_username):
    users = get_all_users()
    print("Users (not blocked):")
    found = False
    for user_id, data in users.items():
        if data["username"] == current_admin_username:
            continue
        if not is_user_blocked(user_id):
            print(f"{user_id}) {data['username']} | {data['email']} | {data['role']}")
            found = True
    if not found:
        print("No users available to block.")


@access_control
def show_users_to_unblock(current_admin_username):
    users = get_all_users()
    print("Blocked users:")
    found = False
    for user_id, data in users.items():
        if data["username"] == current_admin_username:
            continue
        if is_user_blocked(user_id):
            print(f"{user_id}) {data['username']} | {data['email']} | {data['role']}")
            found = True
    if not found:
        print("No blocked users found.")


@access_control
def block_user_by_id(target_user_id, current_admin_username):
    users = get_all_users()

    if target_user_id not in users:
        print("Invalid user ID.")
        return

    if users[target_user_id]["username"] == current_admin_username:
        print("You cannot block yourself.")
        return

    if is_user_blocked(target_user_id):
        print("User is already blocked.")
        return

    db_block_user_by_id(target_user_id)
    print("User blocked successfully.")


@access_control
def unblock_user_by_id(target_user_id, current_admin_username):
    users = get_all_users()

    if target_user_id not in users:
        print("Invalid user ID.")
        return

    if users[target_user_id]["username"] == current_admin_username:
        print("You cannot unblock yourself.")
        return

    if not is_user_blocked(target_user_id):
        print("User is not blocked.")
        return

    db_unblock_user_by_id(target_user_id)
    print("User unblocked successfully.")
