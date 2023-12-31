import json


async def test_create_user(client, get_user_from_database):
    """Test creating user"""
    user_data = {
        "name": "Nikolai",
        "surname": "Nikolaev",
        "email": "nik@mail.ru"
    }
    # test of user creation by client
    response = client.post("/users", data=json.dumps(user_data))
    data_from_response = response.json()
    assert response.status_code == 200
    assert data_from_response["name"] == user_data["name"]
    assert data_from_response["surname"] == user_data["surname"]
    assert data_from_response["email"] == user_data["email"]

    # test of user getting by user_id via get_user_from_database
    users_from_db = await get_user_from_database(data_from_response["user_id"])
    assert len(users_from_db) == 1
    user_from_db = users_from_db[0]
    assert user_from_db["name"] == user_data["name"]
    assert user_from_db["surname"] == user_data["surname"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is True
    assert str(user_from_db["user_id"]) == data_from_response["user_id"]

