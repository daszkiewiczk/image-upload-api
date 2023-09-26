# image-upload-api
DRF project
# Requirements
- docker
- docker compose
# Usage
To build the app:
```bash
docker compose build
```
To run tests:
```bash
docker compose run app sh -c 'python manage.py test'
```
Create a superuser for testing purposes:
```bash
docker compose run app sh -c 'python manage.py createsuperuser'
```
Admin panel is available at [localhost:8000/admin/](localhost:8000/admin/).


To run the app:
```bash
docker compose up
```
Swagger UI is available on [localhost:8000/api/docs/](localhost:8000/api/docs).

Endpoints use token authentication, token can be obtained through /api/user/token/ endpoint after providing user's credentials.


To shutdown the app:
```bash
docker compose down
```