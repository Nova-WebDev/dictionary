import json, bcrypt, time, smtplib, random, base64, binascii
from email.mime.text import MIMEText
from cryptography.hazmat.primitives import serialization
from setting import PRIVATE_KEY_PATH, PRIVATE_KEY_PASSWORD, TOKEN_EXPIRATION, BCRYPT_SALT_ROUNDS, SENDER_EMAIL, \
    APP_PASSWORD
from db.user_db import UserRepository


class TokenService:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    @staticmethod
    def sign_payload(payload_json):
        with open(PRIVATE_KEY_PATH, "rb") as f:
            password_bytes = PRIVATE_KEY_PASSWORD.encode("utf-8")
            private_key = serialization.load_pem_private_key(f.read(), password=password_bytes)
        signature = private_key.sign(payload_json.encode("utf-8"))
        return signature.hex()

    def build_token(self, username):
        role = self._user_repo.get_user_role(username)
        now = int(time.time())
        payload = {
            "sub": username,
            "role": role,
            "iat": now,
            "exp": now + TOKEN_EXPIRATION,
            "iss": "auth"
        }
        payload_json = json.dumps(payload, separators=(",", ":"))
        signature_hex = self.sign_payload(payload_json)
        return payload_json + "." + signature_hex


class AuthService:
    def __init__(self, user_repo: UserRepository, token_service: TokenService, cursor):
        self._user_repo = user_repo
        self._token_service = token_service
        self._cursor = cursor

    def login_user(self, username, password):
        if not self._user_repo.user_exists(username):
            return ""
        creds = self._user_repo.get_user_credentials(username)
        stored_str = creds["password"]
        stored_bytes = safe_decode_password(stored_str)
        if not bcrypt.checkpw(password.encode(), stored_bytes):
            return ""
        return self._token_service.build_token(username)

    def sign_in_user(self, username, email, password):
        if "@" not in email or "." not in email or email.index("@") > email.rindex("."):
            return ""
        if self._user_repo.user_exists(username):
            return ""
        if self._user_repo.email_exists(email):
            return ""
        hashed_bytes = bcrypt.hashpw(password.encode(), bcrypt.gensalt(BCRYPT_SALT_ROUNDS))
        hashed_str = base64.b64encode(hashed_bytes).decode("utf-8")  # ذخیره به صورت TEXT
        self._user_repo.insert_user(username, email, hashed_str, role_name="normal_user")
        self._cursor.connection.commit()
        return self._token_service.build_token(username)


class PasswordResetService:
    def __init__(self, user_repo: UserRepository, token_service: TokenService, cursor):
        self._user_repo = user_repo
        self._token_service = token_service
        self._cursor = cursor

    @staticmethod
    def generate_reset_code():
        return str(random.randrange(1000, 10000))

    @staticmethod
    def send_recovery_email(username, email, code):
        message = MIMEText(
            f"Hi {username}!\n\nYour recovery code is: {code}\n\nIf you didn’t request this, just ignore it.")
        message["Subject"] = "Password Reset Code"
        message["From"] = SENDER_EMAIL
        message["To"] = email
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(message)
        server.quit()

    def initiate_password_reset(self, email):
        if not self._user_repo.email_exists(email):
            return ""
        username = self._user_repo.get_username_by_email(email)
        creds = self._user_repo.get_user_credentials(username)
        stored_str = creds["password"]
        if isinstance(stored_str, str) and stored_str.startswith("!:"):
            return ""
        code = self.generate_reset_code()
        self.send_recovery_email(username, email, code)
        return code

    @staticmethod
    def verify_reset_code(code, user_code):
        if not code:
            return False
        return user_code == code

    def complete_password_reset(self, email, new_password):
        username = self._user_repo.get_username_by_email(email)
        hashed_bytes = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt(BCRYPT_SALT_ROUNDS))
        hashed_str = base64.b64encode(hashed_bytes).decode("utf-8")
        user_id = self._user_repo.get_user_id_by_username(username)
        self._user_repo.update_user_by_id(user_id, {"password": hashed_str})
        self._cursor.connection.commit()
        return self._token_service.build_token(username)


def safe_decode_password(stored_str):
    try:
        return base64.b64decode(stored_str)
    except (binascii.Error, ValueError):
        if isinstance(stored_str, str):
            return stored_str.encode("utf-8")
        return stored_str
