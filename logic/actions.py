import bcrypt, json, time
from setting import MAX_WORD_LENGTH, BCRYPT_SALT_ROUNDS, PUBLIC_KEY_PATH
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
from db.word_db import WordRepository
from db.user_db import UserRepository
from db.role import RoleRepository


class TokenValidator:
    @staticmethod
    def is_token_valid(token: str) -> bool:
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
            return isinstance(exp, int) and int(time.time()) <= exp
        except (ValueError, InvalidSignature, json.JSONDecodeError, FileNotFoundError):
            return False

    @staticmethod
    def extract_payload(token: str):
        if not TokenValidator.is_token_valid(token):
            return None
        try:
            payload_json = token.rsplit(".", 1)[0]
            return json.loads(payload_json)
        except (ValueError, json.JSONDecodeError):
            return None


class AccessControl:
    def __init__(self, allowed_roles):
        self.allowed_roles = allowed_roles

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            token = kwargs.pop("token", "")
            if not token or not TokenValidator.is_token_valid(token):
                return ""
            payload = TokenValidator.extract_payload(token)
            if not payload or payload.get("role") not in self.allowed_roles:
                return ""
            return func(*args, **kwargs)
        return wrapper


class DictionaryActions:
    def __init__(self, cursor):
        self.cursor = cursor
        self.word_repo = WordRepository(cursor)

    @AccessControl(("normal_user", "power_user", "admin"))
    def show_fa_translations(self, en_word):
        if not self.word_repo.english_word_exists(en_word):
            print("Word not found in dictionary.")
            return
        translations = self.word_repo.get_fa_translations_by_en_word(en_word)
        for fa_word, author in translations.items():
            print(f"{fa_word} => {author}")

    @AccessControl(("normal_user", "power_user", "admin"))
    def show_en_translations(self, fa_word):
        if not self.word_repo.persian_word_exists(fa_word):
            print("Word not found in dictionary.")
            return
        translations = self.word_repo.get_en_translations_by_fa_word(fa_word)
        for en_word, author in translations.items():
            print(f"{en_word} => {author}")

    @AccessControl(("normal_user", "power_user", "admin"))
    def print_all_dictionary_words(self):
        words = self.word_repo.get_all_words_with_authors()
        if not words:
            print("Dictionary is empty.")
            return
        for entry in words:
            print(f"{entry['id']}) {entry['english_word']} = {entry['persian_word']} => {entry['author']}")

    @AccessControl(("power_user", "admin"))
    def add_new_word(self, en_word, fa_word, author_username):
        if len(en_word) > MAX_WORD_LENGTH or len(fa_word) > MAX_WORD_LENGTH:
            print(f"Each word must be at most {MAX_WORD_LENGTH} characters.")
            return
        self.word_repo.insert_word(en_word, fa_word, author_username)
        self.cursor.connection.commit()
        print("Word added successfully.")

    @AccessControl(("power_user",))
    def edit_own_word(self, word_id, new_en, new_fa, author_username):
        if not self.word_repo.author_has_words(author_username):
            print("You haven't submitted any words yet.")
            return
        if not self.word_repo.word_id_belongs_to_author(word_id, author_username):
            print("You are not allowed to edit this word.")
            return
        if len(new_en) > MAX_WORD_LENGTH or len(new_fa) > MAX_WORD_LENGTH:
            print(f"Each word must be at most {MAX_WORD_LENGTH} characters.")
            return
        self.word_repo.update_word_by_id(word_id, {"english_word": new_en, "persian_word": new_fa})
        self.cursor.connection.commit()
        print("Word updated successfully.")

    @AccessControl(("admin",))
    def edit_any_word(self, word_id, new_en, new_fa):
        if not self.word_repo.word_id_exists(word_id):
            print("Word ID not found.")
            return
        if len(new_en) > MAX_WORD_LENGTH or len(new_fa) > MAX_WORD_LENGTH:
            print(f"Each word must be at most {MAX_WORD_LENGTH} characters.")
            return
        self.word_repo.update_word_by_id(word_id, {"english_word": new_en, "persian_word": new_fa})
        self.cursor.connection.commit()
        print("Word updated successfully.")

    @AccessControl(("power_user",))
    def delete_own_word(self, word_id, author_username):
        if not self.word_repo.author_has_words(author_username):
            print("You haven't submitted any words yet.")
            return
        if not self.word_repo.word_id_belongs_to_author(word_id, author_username):
            print("You are not allowed to delete this word.")
            return
        self.word_repo.delete_word_by_id(word_id)
        self.cursor.connection.commit()
        print("Word deleted successfully.")

    @AccessControl(("admin",))
    def delete_any_word(self, word_id):
        if not self.word_repo.word_id_exists(word_id):
            print("Word ID not found.")
            return
        self.word_repo.delete_word_by_id(word_id)
        self.cursor.connection.commit()
        print("Word deleted successfully.")


class UserActions:
    def __init__(self, cursor):
        self.cursor = cursor
        self.user_repo = UserRepository(cursor)
        self.role_repo = RoleRepository(cursor)

    @AccessControl(("admin",))
    def show_all_users(self, current_username):
        users = self.user_repo.get_all_users()
        for user_id, data in users.items():
            if data["username"] == current_username:
                continue
            print(f"{user_id}) {data['username']} | {data['email']} | {data['role']}")

    @AccessControl(("admin",))
    def create_new_user(self, new_username, new_email, new_password, role_id,
                        current_admin_username, confirm_admin_downgrade=False):
        if self.user_repo.user_exists(new_username):
            print("Username already exists.")
            return
        if self.user_repo.email_exists(new_email):
            print("Email already exists.")
            return
        hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt(BCRYPT_SALT_ROUNDS)).decode()
        if not self.role_repo.role_id_exists(role_id):
            print("Role ID not found.")
            return
        selected_role_name = self.role_repo.get_role_name_by_id(role_id)
        if selected_role_name == "admin":
            if not confirm_admin_downgrade:
                print("Operation cancelled. Admin downgrade not confirmed.")
                return
            self.user_repo.insert_user(new_username, new_email, hashed_password, "admin")
            self.cursor.connection.commit()
            current_admin_id = self.user_repo.get_user_id_by_username(current_admin_username)
            self.user_repo.update_user_by_id(current_admin_id, {"role_name": "power_user"})
            self.cursor.connection.commit()
            print("User created as admin. Your role has been downgraded to power_user.")
            return
        self.user_repo.insert_user(new_username, new_email, hashed_password, selected_role_name)
        self.cursor.connection.commit()
        print(f"User created successfully with role '{selected_role_name}'.")

    @AccessControl(("admin",))
    def change_user_role(self, target_user_id, new_role_id, current_admin_username, confirm_admin_downgrade=False):
        users = self.user_repo.get_all_users()
        if target_user_id not in users or users[target_user_id]["username"] == current_admin_username:
            print("Invalid user ID.")
            return
        if not self.role_repo.role_id_exists(new_role_id):
            print("Role ID not found.")
            return
        selected_role_name = self.role_repo.get_role_name_by_id(new_role_id)
        if selected_role_name == "admin":
            if not confirm_admin_downgrade:
                print("Operation cancelled.")
                return
            self.user_repo.update_user_by_id(target_user_id, {"role_name": "admin"})
            self.cursor.connection.commit()
            current_admin_id = self.user_repo.get_user_id_by_username(current_admin_username)
            self.user_repo.update_user_by_id(current_admin_id, {"role_name": "power_user"})
            self.cursor.connection.commit()
            print("Role updated. You are now a power_user.")
            return
        self.user_repo.update_user_by_id(target_user_id, {"role_name": selected_role_name})
        self.cursor.connection.commit()
        print(f"Role updated successfully to '{selected_role_name}'.")


class BlockActions:
    def __init__(self, cursor):
        self.cursor = cursor
        self.user_repo = UserRepository(cursor)

    @AccessControl(("admin",))
    def show_blocked_users(self):
        blocked_users = self.user_repo.db_get_all_blocked_users()
        if not blocked_users:
            print("No blocked users found.")
            return
        for user_id, username in blocked_users.items():
            print(f"{user_id}) {username}")

    @AccessControl(("admin",))
    def show_unblocked_users(self, current_admin_username):
        users = self.user_repo.get_all_users()
        found = False
        for user_id, data in users.items():
            if data["username"] == current_admin_username:
                continue
            if not self.user_repo.is_user_blocked(user_id):
                print(f"{user_id}) {data['username']} | {data['email']} | {data['role']}")
                found = True
        if not found:
            print("No users available to block.")

    @AccessControl(("admin",))
    def show_users_to_unblock(self, current_admin_username):
        users = self.user_repo.get_all_users()
        found = False
        for user_id, data in users.items():
            if data["username"] == current_admin_username:
                continue
            if self.user_repo.is_user_blocked(user_id):
                print(f"{user_id}) {data['username']} | {data['email']} | {data['role']}")
                found = True
        if not found:
            print("No blocked users found.")

    @AccessControl(("admin",))
    def block_user_by_id(self, target_user_id, current_admin_username):
        users = self.user_repo.get_all_users()
        if target_user_id not in users:
            print("Invalid user ID.")
            return
        if users[target_user_id]["username"] == current_admin_username:
            print("You cannot block yourself.")
            return
        if self.user_repo.is_user_blocked(target_user_id):
            print("User is already blocked.")
            return
        self.user_repo.db_block_user_by_id(target_user_id)
        self.cursor.connection.commit()
        print("User blocked successfully.")

    @AccessControl(("admin",))
    def unblock_user_by_id(self, target_user_id, current_admin_username):
        users = self.user_repo.get_all_users()
        if target_user_id not in users:
            print("Invalid user ID.")
            return
        if users[target_user_id]["username"] == current_admin_username:
            print("You cannot unblock yourself.")
            return
        if not self.user_repo.is_user_blocked(target_user_id):
            print("User is not blocked.")
            return
        self.user_repo.db_unblock_user_by_id(target_user_id)
        self.cursor.connection.commit()
        print("User unblocked successfully.")
