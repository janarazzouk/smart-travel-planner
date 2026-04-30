import requests


BASE_URL = "http://127.0.0.1:8000/api"


def main() -> None:
    email = "test@example.com"
    password = "password123"

    print("Registering...")
    register_response = requests.post(
        f"{BASE_URL}/auth/register",
        json={"email": email, "password": password},
        timeout=20,
    )
    print("Register:", register_response.status_code, register_response.text)

    print("Logging in...")
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": email, "password": password},
        timeout=20,
    )
    print("Login:", login_response.status_code, login_response.text)

    login_response.raise_for_status()
    token = login_response.json()["access_token"]

    print("Calling agent...")
    agent_response = requests.post(
        f"{BASE_URL}/agent/run",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "input_text": "I want a warm adventure trip with hiking and outdoor activities."
        },
        timeout=60,
    )

    print("Agent:", agent_response.status_code)
    print(agent_response.text)


if __name__ == "__main__":
    main()