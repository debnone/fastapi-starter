import pytest
from app import schemas
from .database import client, session

# we import session from database.py 👆, even though we are not using it in this file,
# but because client is dependent on session.


@pytest.fixture
def test_user(client):
    user_data = {
        "email": "dabsantamer@yahoo.com",
        "password": "12345678",
    }
    response = client.post("/users/", json=user_data)

    assert response.status_code == 201  # created
    print(response.json())
    return


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "email": "dabsantamer@yahoo.com",
            "password": "12345678",
            "validate_email_code": "",
        },
    )
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == "dabsantamer@yahoo.com"
    assert response.status_code == 201


def test_login_user_(client, test_user):
    response = client.post(
        "/login", data={"username": "dabsantamer@yahoo.com", "password": "12345678",},
    )

    assert response.status_code == 200
