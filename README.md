# Library Service API
 
A REST API for managing a library's book catalog and borrowings. Users can browse books and borrow/return them; admins manage the catalog and see all borrowings.
 
## Features
- User registration and JWT-based authentication
- Book catalog (list/detail public, write access admin-only), filterable by title/author
- Borrowing a book (checks and decrements available inventory)
- Returning a book (increments inventory back)
- Filtering borrowings by status (`is_active`) and, for admins, by user (`user_id`)
- Pagination on books and borrowings lists (10 per page by default, configurable via `page_size`)
- Interactive API docs (Swagger UI / ReDoc) via drf-spectacular
- Django admin panel for managing data directly
- CI pipeline (GitHub Actions) running Black, Flake8, and the test suite on every PR
## Tech Stack
- Python / Django 6.0
- Django REST Framework
- JWT auth (`djangorestframework-simplejwt`)
- drf-spectacular (OpenAPI schema, Swagger UI, ReDoc)
- PostgreSQL
## Setup (Docker)
 
```bash
git clone https://github.com/misha-cw/library-service.git
cd library-service
 
cp .env.sample .env
docker-compose up --build
```
 
Runs at `http://127.0.0.1:8001/` (the `web` service maps container port `8000` to host port `8001`). Migrations run automatically on startup.
 
Create an admin user (needed to manage books, or via the admin panel):
 
```bash
docker-compose exec web python manage.py createsuperuser
```
 
Django admin panel: `http://127.0.0.1:8001/admin/`
 
## Setup (local, no Docker)
 
Requires a running PostgreSQL instance.
 
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
 
pip install -r requirements.txt
```
 
Set these env vars before running (or use a `.env` loader):
 
| Variable | Description | Default |
|---|---|---|
| `SECRET_KEY` | Django secret key | — (required) |
| `POSTGRES_DB` | Database name | `library` |
| `POSTGRES_USER` | Database user | `library` |
| `POSTGRES_PASSWORD` | Database password | `library` |
| `POSTGRES_HOST` | Database host | `db` |
| `POSTGRES_PORT` | Database port | `5432` |
 
```bash
python manage.py migrate
python manage.py runserver
```
 
Runs at `http://127.0.0.1:8000/`.
 
## API Docs
 
Once the server is running, the interactive API documentation is available at:
 
| Format | Endpoint |
|---|---|
| OpenAPI schema (raw) | `/api/docs/` |
| Swagger UI | `/api/docs/swagger/` |
| ReDoc | `/api/docs/redoc/` |
 
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
| GET | `/api/books/` | List books (filter by `title`, `author`) |
| POST | `/api/books/` | Add book (admin) |
| GET/PUT/DELETE | `/api/books/{id}/` | Book detail (write = admin) |
| GET | `/api/borrowings/` | List your borrowings |
| POST | `/api/borrowings/` | Borrow a book |
| GET | `/api/borrowings/{id}/` | Borrowing detail |
| POST | `/api/borrowings/{id}/return/` | Return a book |
 
Filters: `GET /api/borrowings/?is_active=true`, and `?user_id=` (admin only). `GET /api/books/?title=&author=`. All list endpoints accept `?page=` and `?page_size=` (max 100).
 
## Example: borrow a book
 
```
POST /api/borrowings/
Authorization: Bearer <access_token>
```
```json
{
  "book": 1,
  "expected_return_date": "2026-07-15"
}
```
 
## Permissions
 
| Role | Books | Borrowings |
|---|---|---|
| Anonymous | Read-only | No access |
| Authenticated user | Read-only | Own borrowings only |
| Admin (`is_staff=true`) | Full access | All borrowings |
 
## Tests
 
```bash
python manage.py test
# or, in Docker:
docker-compose exec web python manage.py test
```