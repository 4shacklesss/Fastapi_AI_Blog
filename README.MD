# FastAPI AI Blog

A full-stack blog application built with FastAPI, asynchronous SQLAlchemy, and server-rendered Jinja2 templates. It includes a responsive web interface and a REST API for managing users, posts, and account settings.

> **Project status:** Core blogging and account features are implemented, including email-based password recovery.
## Features

- **Authentication** — User registration, email-based login, JWT access tokens, and Argon2 password hashing.
- **Post management** — Create, read, update, and delete posts, with ownership checks for editing and deletion.
- **Pagination** — Paginated post APIs and “Load More” functionality on the homepage and user post pages.
- **Account management** — Update usernames and email addresses, change passwords, and delete accounts.
- **Profile pictures** — Upload, replace, and remove avatars. Images are cropped to 300 × 300 pixels and saved as JPEG files, with a default upload limit of 5 MiB.
- **Password recovery** — Email-based password resets using expiring tokens stored as SHA-256 hashes. Reset emails are sent through background tasks.
- **Responsive interface** — Bootstrap layouts, light and dark themes, modal dialogs, and HTML error pages.
- **API documentation** — Interactive Swagger UI and ReDoc documentation.

## Tech Stack

| Component | Technology |
| --- | --- |
| Runtime | Python 3.14+ |
| Backend | FastAPI, Uvicorn |
| Database | SQLite, SQLAlchemy 2.x Async, aiosqlite |
| Validation and configuration | Pydantic, pydantic-settings |
| Authentication | PyJWT, pwdlib with Argon2 |
| Frontend | Jinja2, Bootstrap 5.3, JavaScript |
| Image processing | Pillow |
| Email | aiosmtplib |
| Dependency management | 

## API Overview

Protected endpoints require the following header:

```http
Authorization: Bearer <access_token>
```

### Users and Authentication

| Method | Endpoint | Description | Access |
| --- | --- | --- | --- |
| `POST` | `/api/users` | Register a user | Public |
| `POST` | `/api/users/token` | Log in and receive an access token | Public |
| `GET` | `/api/users/me` | Get the current user's profile | Authenticated |
| `PATCH` | `/api/users/me/password` | Change the current user's password | Authenticated |
| `POST` | `/api/users/forgot-password` | Request a password reset email | Public |
| `POST` | `/api/users/reset-password` | Reset a password using a reset token | Public |
| `GET` | `/api/users/{user_id}` | Get a user's public profile | Public |
| `GET` | `/api/users/{user_id}/posts` | List a user's posts | Public |
| `PATCH` | `/api/users/{user_id}` | Update account details | Account owner |
| `DELETE` | `/api/users/{user_id}` | Delete an account and its posts | Account owner |
| `PATCH` | `/api/users/{user_id}/picture` | Upload or replace an avatar | Account owner |
| `DELETE` | `/api/users/{user_id}/picture` | Remove an avatar | Account owner |

The login endpoint accepts an `application/x-www-form-urlencoded` body with `username` and `password` fields. **Use the user's email address as the `username` value**, including when authorizing through Swagger UI.

Avatar uploads use `multipart/form-data` with a file field named `file`.

### Posts

| Method | Endpoint | Description | Access |
| --- | --- | --- | --- |
| `GET` | `/api/posts` | List posts | Public |
| `POST` | `/api/posts` | Create a post | Authenticated |
| `GET` | `/api/posts/{post_id}` | Get a post | Public |
| `PUT` | `/api/posts/{post_id}` | Replace a post's title and content | Post author |
| `PATCH` | `/api/posts/{post_id}` | Partially update a post | Post author |
| `DELETE` | `/api/posts/{post_id}` | Delete a post | Post author |

Post list endpoints support:

- `skip`: Number of posts to skip, starting at `0`.
- `limit`: Number of posts to return, from `1` to `100`.

Paginated responses contain `posts`, `total`, `skip`, `limit`, and `has_more`.

See `/docs` for request schemas and response details.

## Project Structure

```text
Fastapi_AI_Blog/
├── main.py                 # Application setup, page routes, and error handling
├── config.py               # Environment-based settings
├── database.py             # Async database engine and sessions
├── models.py               # User, post, and password reset token models
├── schemas.py              # Request and response schemas
├── auth.py                 # Password hashing, JWTs, and authentication dependencies
├── email_utils.py          # SMTP delivery and password reset emails
├── image_utils.py          # Avatar processing and file management
├── routers/
│   ├── users.py            # User, authentication, avatar, and password APIs
│   └── posts.py            # Post APIs and pagination
├── templates/              # Jinja2 page and email templates
├── static/                 # Styles, scripts, icons, and default avatar
├── media/profile_pics/     # Uploaded avatars; created locally
├── populate_db.py          # Demo data population script
├── pyproject.toml          # Project metadata and dependencies
└── uv.lock                 # Locked dependencies
```

## Future Improvements

- Integrate AI-assisted blogging features.
- Add automated tests for authentication, permissions, and password recovery.
- Introduce database migrations.
- Improve error handling and token revocation.
- Add deployment configuration.
