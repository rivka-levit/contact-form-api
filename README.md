# Form Submission RestAPI

### Store and manage messages from submission forms

#### Description:

- PostgreSQL database to store messages.
- Django, Rest-Framework backend.
- Automatic Spectacular forntend.
- Dockerized app.
- Unit tests.

Command to run the app:

```commandline
    docker compose up
```

Command to run tests:
```commandline
    docker compose run --rm app sh -c "python manage.py test"
```