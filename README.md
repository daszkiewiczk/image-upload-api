# image-upload-api
An API that allows users to upload images in JPEG or PNG format, implmented in django-rest-framework.
Approx. time to complete the project: ~10h work over 2 days

# Implemented features
- users can upload images via POST /api/images
- users can list their images (and links) via GET /api/images
- users can create an expiring link via POST /api/images/links
- accout tiering (Basic, Premium, Enterprise) is implemented
- additional tiers and thumbnail sizes can be added via admin panel
- users are added via admin panel
- token authentication is enabled, user can get token via GET /api/user/token

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
Admin panel is available at [localhost:8000/admin/](http://localhost:8000/admin/).


To run the app:
```bash
docker compose up
```
Swagger UI is available on [localhost:8000/api/docs/](http://localhost:8000/api/docs).

Endpoints use token authentication, token can be obtained through /api/user/token/ endpoint after providing user's credentials.


To shutdown the app:
```bash
docker compose down
```