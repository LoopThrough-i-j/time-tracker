import json
import time
from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
import jwt

from app.utils.encryption import EncryptionService

from constants.exceptions import BadRequestError, NotFoundError
from database.mongodb.actions.employee import EmployeeActions
from database.mongodb.models.employee import Employee
from environment import EnvironmentVariables


class AuthService:
    def __init__(self):
        self.employee_actions = EmployeeActions()
        self.secret_key = EnvironmentVariables.SECRET_KEY
        self.encryption_service = EncryptionService(self.secret_key.encode())
        self.algorithm = "HS256"
        self.access_token_expire_hours = 24

    def generate_signup_token(self, employee_id: str, expiry_hours: int = 24) -> str:
        expiry_timestamp = int(time.time()) + (expiry_hours * 3600)
        payload = {"employee_id": employee_id, "expiry": expiry_timestamp}
        return self.encryption_service.encrypt(json.dumps(payload))

    def decrypt_signup_token(self, token: str) -> dict:
        try:
            decrypted_data = self.encryption_service.decrypt(token)
            payload = json.loads(decrypted_data)

            current_time = int(time.time())
            if current_time > payload["expiry"]:
                raise ValueError("Token has expired")

            return payload
        except (json.JSONDecodeError, KeyError):
            raise ValueError("Invalid token format")
        except Exception:
            raise ValueError("Invalid or corrupted token")

    def get_employee_by_id(self, employee_id: str) -> Optional[Employee]:
        return self.employee_actions.get_by_id(employee_id)

    def update_employee_password(self, email: str, password: str) -> Employee:
        existing_employee = self.employee_actions.get_by_email(email)

        if not existing_employee:
            raise NotFoundError("Employee not found. Please contact administrator to be invited first.")

        hashed_password = self._hash_password(password)

        update_data = {"password": hashed_password}
        employee = self.employee_actions.update_fields(existing_employee.id, update_data)

        return employee

    def authenticate_employee(self, email: str, password: str) -> tuple[Employee, str]:
        employee = self.employee_actions.get_by_email(email)
        if not employee:
            raise NotFoundError("Employee not found")

        if employee.password is None:
            raise BadRequestError("Signed up Pending. Please sign up first.")

        if not self._verify_password(password, employee.password):
            raise BadRequestError("Invalid credentials")

        access_token = self._create_access_token(employee.id, employee.email)

        return employee, access_token

    def verify_token(self, token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise BadRequestError("Token has expired")
        except jwt.InvalidTokenError:
            raise BadRequestError("Invalid token")

    def _hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def _verify_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

    def _create_access_token(self, employee_id: str, email: str) -> str:
        expire = datetime.now(tz=timezone.utc) + timedelta(hours=self.access_token_expire_hours)
        payload = {"employee_id": employee_id, "email": email, "exp": expire, "iat": datetime.now(tz=timezone.utc)}
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
