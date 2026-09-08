def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to DevTrack!"
    }


def test_create_task(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Learn pytest",
            "priority": "High"
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Learn pytest"
    assert response.json()["priority"] == "High"


def test_get_tasks(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_task(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Test individual task",
            "priority": "Medium"
        }
    )

    task_id = response.json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["title"] == "Test individual task"
    assert response.json()["priority"] == "Medium"


def test_get_task_not_found(client):
    response = client.get("/tasks/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Task not found"
    }


def test_update_task(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Old title",
            "priority": "Low"
        }
    )

    task_id = response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Updated title",
            "priority": "High"
        }
    )

    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["title"] == "Updated title"
    assert response.json()["priority"] == "High"


def test_update_task_not_found(client):
    response = client.put(
        "/tasks/999999",
        json={
            "title": "Does not exist",
            "priority": "High"
        }
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Task not found"
    }


def test_delete_task(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Task to delete",
            "priority": "Low"
        }
    )

    task_id = response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Task deleted successfully"
    }

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 404