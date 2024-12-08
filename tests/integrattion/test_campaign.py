from datetime import datetime, timedelta

def test_create_campaign(client):
    # Create User
    user_data = {"username": "testuser", "email": "testuser@example.com", "password": "securepassword"}
    user_response = client.post("/users/", json=user_data)
    assert user_response.status_code == 201
    user = user_response.json()

    # Log in user and get Token
    login_data = {"username": user_data["username"], "password": user_data["password"]}
    login_response = client.post("/login", data=login_data)
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # current time
    time_now = datetime.now()

    # Time + 5 Minutes
    time_plus_5_min = time_now + timedelta(minutes=5)

    header = {"Authorization": f"Bearer {token}"}
    campaig_data = {
        "name": "TestCampaign",
        "campaign_end": time_plus_5_min,
        "max_ticket": 100,
        "min_ticket": 0,
        "max_ticket_per_user": 1,
        "prizes": [
            {
            "product_name": "Macbook Pro",
            "product_description": "Is the newest Macbook"
            },
            {
            "product_name": "Ipad",
            "product_description": "Is the newest Iphone"
            },
            {
            "product_name": "Iphone",
            "product_description": "Is the newest Iphone"
            },
        ]
    }
    create_response = client.post(
        "/campaign/",
        json=campaig_data,
        headers=header
    )
    assert create_response.status_code == 201
    assert create_response.json()["name"] == "TestCampaign"
    assert create_response.json()["email"] == "testuser@example.com"


