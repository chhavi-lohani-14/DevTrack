from fastapi.testclient import TestClient


def register_user(client, username="testuser", password="password123"):
    response = client.post(
        "/register",
        json={
            "username": username,
            "password": password
        }
    )
    return response


def login_user(client, username="testuser", password="password123"):
    response = client.post(
        "/login",
        data={
            "username": username,
            "password": password
        }
    )
    return response.json()["access_token"]


def auth_headers(token):
    return {
        "Authorization": f"Bearer {token}"
    }


def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to DevTrack!"
    }


def test_register_user(client):
    response = register_user(client)

    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert response.json()["role"] == "user"
    assert "hashed_password" not in response.json()


def test_register_duplicate_user(client):
    register_user(client)

    response = register_user(client)

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Username already exists"
    }


def test_login(client):
    register_user(client)

    response = client.post(
        "/login",
        data={
            "username": "testuser",
            "password": "password123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_wrong_password(client):
    register_user(client)

    response = client.post(
        "/login",
        data={
            "username": "testuser",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_create_task(client):
    register_user(client)
    token = login_user(client)

    response = client.post(
        "/tasks",
        json={
            "title": "Learn pytest",
            "priority": "High"
        },
        headers=auth_headers(token)
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Learn pytest"
    assert response.json()["priority"] == "High"
    assert response.json()["user_id"] == 1


def test_get_tasks(client):
    register_user(client)
    token = login_user(client)

    client.post(
        "/tasks",
        json={
            "title": "Test task",
            "priority": "Medium"
        },
        headers=auth_headers(token)
    )

    response = client.get(
        "/tasks",
        headers=auth_headers(token)
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_task(client):
    register_user(client)
    token = login_user(client)

    create_response = client.post(
        "/tasks",
        json={
            "title": "Individual task",
            "priority": "Medium"
        },
        headers=auth_headers(token)
    )

    task_id = create_response.json()["id"]

    response = client.get(
        f"/tasks/{task_id}",
        headers=auth_headers(token)
    )

    assert response.status_code == 200
    assert response.json()["id"] == task_id


def test_get_task_not_found(client):
    register_user(client)
    token = login_user(client)

    response = client.get(
        "/tasks/999999",
        headers=auth_headers(token)
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Task not found"
    }


def test_update_task(client):
    register_user(client)
    token = login_user(client)

    create_response = client.post(
        "/tasks",
        json={
            "title": "Old title",
            "priority": "Low"
        },
        headers=auth_headers(token)
    )

    task_id = create_response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Updated title",
            "priority": "High"
        },
        headers=auth_headers(token)
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Updated title"
    assert response.json()["priority"] == "High"


def test_delete_task(client):
    register_user(client)
    token = login_user(client)

    create_response = client.post(
        "/tasks",
        json={
            "title": "Task to delete",
            "priority": "Low"
        },
        headers=auth_headers(token)
    )

    task_id = create_response.json()["id"]

    response = client.delete(
        f"/tasks/{task_id}",
        headers=auth_headers(token)
    )

    assert response.status_code == 200

    response = client.get(
        f"/tasks/{task_id}",
        headers=auth_headers(token)
    )

    assert response.status_code == 404


def test_unauthorized_access(client):
    response = client.get("/tasks")

    assert response.status_code == 401


def test_user_cannot_access_another_users_task(client):
    register_user(client, "user1", "password123")
    token1 = login_user(client, "user1", "password123")

    create_response = client.post(
        "/tasks",
        json={
            "title": "Private task",
            "priority": "High"
        },
        headers=auth_headers(token1)
    )

    task_id = create_response.json()["id"]

    register_user(client, "user2", "password123")
    token2 = login_user(client, "user2", "password123")

    response = client.get(
        f"/tasks/{task_id}",
        headers=auth_headers(token2)
    )

    assert response.status_code == 404

def test_regular_user_cannot_access_admin_endpoint(client):
    register_user(client)
    token = login_user(client)

    response = client.get(
        "/admin/tasks",
        headers=auth_headers(token)
    )

    assert response.status_code == 403
    assert response.json() == {
        "detail": "Admin access required"
    }

def test_admin_can_access_all_tasks(client, db):
    register_user(client, "admin", "password123")

    from app.models import User

    admin = db.query(User).filter(
        User.username == "admin"
    ).first()

    admin.role = "admin"
    db.commit()

    token = login_user(client, "admin", "password123")

    response = client.get(
        "/admin/tasks",
        headers=auth_headers(token)
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)