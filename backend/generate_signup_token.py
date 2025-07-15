from services.auth import AuthService


def generate_signup_url(employee_id: str, base_url: str = "http://localhost:8080") -> str:
    auth_service = AuthService()
    token = auth_service.generate_signup_token(employee_id)
    return f"{base_url}/auth/signup?token={token}"


if __name__ == "__main__":
    employee_id = "60f1c2b5e1b9a123456789ab"
    signup_url = generate_signup_url(employee_id)
    print(f"Signup URL for employee {employee_id}:")
    print(signup_url)
