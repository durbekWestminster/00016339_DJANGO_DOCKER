EVENT PLANNER

Event planning web application built with Django. Users can create events, browse them, and RSVP. Built for learning containerized deployment and CI/CD.

Live at events.dappsio.com


FEATURES

User registration and login.
Create, edit, and delete events. Only the organizer can modify their own events.
RSVP and cancel RSVP to any event.
Event categories.
My Events page showing organized and attending events.
Admin panel.
Redis-backed sessions and caching.
Health check endpoint at /health/.


TECHNOLOGIES

Django 4.2, Python 3.13
PostgreSQL 17
Redis 7
Gunicorn 23.0
Nginx (Alpine)
Docker, Docker Compose
GitHub Actions
GitHub Container Registry


LOCAL SETUP

Requirements: Docker, Docker Compose, Git.

1. Clone the repository.
2. Create a .env file in the project root with the variables listed in the Environment Variables section below.
3. Run: docker compose -f docker-compose.yml.dev up --build
4. Run: docker exec eventplanner-web python manage.py migrate
5. Run: docker exec eventplanner-web python manage.py createsuperuser
6. Open http://localhost:8082


DEPLOYMENT

Automated via GitHub Actions. On every push to main, the pipeline builds the Docker image, pushes it to GitHub Container Registry, SSHs into the server, pulls the image, and restarts the containers. Migrations and collectstatic run automatically after deployment.

The server has a host Nginx on port 80 that proxies requests for events.dappsio.com to the containerized Nginx on port 8011. The containerized Nginx serves static and media files from shared Docker volumes and proxies everything else to Gunicorn.

Four containers run in production: PostgreSQL, Django with Gunicorn, Redis, and Nginx. All on a bridge network.


ENVIRONMENT VARIABLES

DJANGO_SECRET_KEY    - Django secret key for signing
DEBUG                - True for development, False for production
DJANGO_LOGLEVEL      - Logging level (info)
DATABASE_ENGINE      - Database backend (postgresql)
DATABASE_NAME        - Database name (eventplannerdb)
DATABASE_USERNAME    - Database user (dbuser)
DATABASE_PASSWORD    - Database password
DATABASE_HOST        - Database host (db in Docker, 127.0.0.1 locally)
DATABASE_PORT        - Database port (5432)
REDIS_URL            - Redis connection string (set in docker-compose.yml)
