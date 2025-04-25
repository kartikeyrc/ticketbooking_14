# Ticket Booking System

A Django-based ticket booking system with MySQL, Docker, and Jenkins CI/CD support.

---

## Features
- Book movie tickets online
- User authentication
- MySQL database
- Dockerized for easy deployment
- Jenkins pipeline for CI/CD

---

## Local Setup

1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd ticket_booking_system
   ```

2. **Create a virtual environment and activate it:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up your `.env` file:**
   Copy `.env.example` to `.env` and fill in your values.

5. **Configure MySQL:**
   - Make sure MySQL is running and a database named `ticket_db` exists.
   - Update your `settings.py` or `.env` with your MySQL credentials.

6. **Run migrations:**
   ```sh
   python manage.py migrate
   ```

7. **Create a superuser (optional):**
   ```sh
   python manage.py createsuperuser
   ```

8. **Add sample movies (optional):**
   ```sh
   python manage.py add_sample_movies
   ```

9. **Run the server:**
   ```sh
   python manage.py runserver
   ```

---

## Docker Setup

1. **Build and start the containers:**
   ```sh
   docker-compose up --build
   ```

2. **The app will be available at** [http://localhost:8000](http://localhost:8000)

3. **To run management commands:**
   ```sh
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser
   docker-compose exec web python manage.py add_sample_movies
   ```

---

## Jenkins CI/CD

- The `jenkinsfile` is set up for basic build, lint, test, and deploy using Docker Compose.
- Make sure your Jenkins agent has Docker and Python installed.

---

## Environment Variables

- `DJANGO_DB_HOST` (default: `localhost` or `db` in Docker)
- `DJANGO_DB_NAME` (default: `ticket_db`)
- `DJANGO_DB_USER` (default: `user`)
- `DJANGO_DB_PASSWORD` (default: `password`)
- `DJANGO_SECRET_KEY` (set your own secret key)
- `DJANGO_DEBUG` (default: `True`)

---

## Notes
- For production, set `DEBUG=False` and use a strong `SECRET_KEY`.
- Update allowed hosts in `settings.py` for deployment.
- Static files are collected automatically in Docker build.

---

## License
MIT 