# GlasGo
External Sources Used:
- Django
- Twitter Bootstrap 4
- Django Registration Redux
- Django Widget Tweaks
- Pillow
- pytz
- sqlparse
- JQuery
  - DateTimePicker Plugin
  - JQuery Validate Plugin
- AJAX
- Bs-custom-file-input (JS Plugin)

To build the database:
```
>python manage.py migrate
>python manage.py makemigrations glasgo
>python manage.py migrate
```

To test the admin functionality, an admin account will have to be created:
`>python manage.py createsuperuser`

`populate_glasgo.py` will populate the database with a number of sample tags, attractions, users, and votes for demonstration purposes.  The data and images for these attractions were taken from google.  The population script may take around 15 minutes to finish populating the votes.
