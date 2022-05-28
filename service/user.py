import base64
import hashlib
import hmac

from helpers.constants import PWD_HASH_ITERATIONS, PWD_HASH_SALT
from dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_by_username(self, username):
        return self.dao.get_by_username(username)

    def get_all(self):
        return self.dao.get_all()

    def create(self, user_d):
        user_d["password"] = self.generate_user_password(user_d.get("password"))
        return self.dao.create(user_d)

    def delete(self, uid):
        self.dao.delete(uid)

    def update(self, user_d):
        user_d["password"] = self.generate_user_password(user_d.get("password"))
        self.dao.update(user_d)
        return self.dao

    def generate_hash_digest(self, password):
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return hash_digest

    def generate_user_password(self, password):
        hash_digest = self.generate_hash_digest(password)
        return base64.b64encode(hash_digest)

    def compare_passwords(self, password_hash, other_password) -> bool:
        decoded_password_hash = base64.b64decode(password_hash)
        other_password_hash = self.generate_hash_digest(other_password)
        return hmac.compare_digest(decoded_password_hash, other_password_hash)

