# Library Service API

A simple REST API for managing a library — books and borrowings. Built with Django REST Framework and JWT auth. Study project.

## Tech Stack
- Python / Django 6.0
- Django REST Framework
- JWT auth (`djangorestframework-simplejwt`)
- SQLite (dev)

## Setup

```bash
git clone https://github.com/misha-cw/library-service.git
cd library-service

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Runs at `http://127.0.0.1:8000/`.

## Auth

Register, then get a token:

```
POST /api/users/            -> {"email": "...", "password": "..."}
POST /api/users/token/      -> {"email": "...", "password": "..."}
```

Use the returned `access` token on protected requests:

```
Authorization: Bearer <access_token>
```

## Main Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/users/` | Register |
| POST | `/api/users/token/` | Get JWT tokens |
| POST | `/api/users/token/refresh/` | Refresh token |
| GET/PUT | `/api/users/me/` | Your profile |
| GET | `/api/books/` | List books |
| POST | `/api/books/` | Add book (admin) |
| GET/PUT/DELETE | `/api/books/{id}/` | Book detail (write = admin) |
| GET | `/api/borrowings/` | List your borrowings |
| POST | `/api/borrowings/` | Borrow a book |
| GET | `/api/borrowings/{id}` | Borrow detail |
| POST | `/api/borrowings/{id}/return/` | Return a book |

Filters: `GET /api/borrowings/?is_active=true`, and `?user_id=` (admin only).

## Tests

```bash
python manage.py test
```
