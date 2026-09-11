# DevTrack

DevTrack is a task management REST API that I built while learning and working with FastAPI.

The project started as a basic CRUD API and was later extended with authentication, user-specific tasks, role-based access control, automated testing, and GitHub Actions CI.

## What it does

- Register and log in users
- Hash passwords before storing them
- Authenticate requests using JWT tokens
- Create, view, update and delete tasks
- Keep tasks associated with their users
- Prevent users from accessing other users' tasks
- Provide an admin-only endpoint for viewing all tasks
- Validate API requests using Pydantic
- Run automated API tests using pytest
- Run tests automatically through GitHub Actions

## Tech used

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT / OAuth2
- pwdlib / Argon2
- pytest
- GitHub Actions

## Project structure

```text
DevTrack/
│
├── app/
│   ├── auth.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
│
├── tests/
│   ├── conftest.py
│   └── test_tasks.py
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── .gitignore
├── requirements.txt
└── README.md