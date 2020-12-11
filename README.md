#  CokbookAPI

Grown from the requirement to permanently store recipes we cooked and appreciated, a decent data structure needed to be created.
Based on the requirements on ease-of-use, stability and relational data models Django and PostgreSQL were chosen as the 
technology of choice.

# Configuration

In order to provide this project as a public repository all configurations were extracted from the `settings.py`
and referenced from outside. To use this project simply create a `config.py` file in the root folder and fill
it with the relevant properties. An example can be found here:

```
from pathlib import Path
import os

# A secret key that is used by all endpoints in order to protect from
# non authorised access.
SECRET_KEY = 'secret'
# A list of hosts that are allowed as root url.
ALLOWED_HOSTS = ['127.0.0.1']
# Indicates if additional logging to the user is activated.
DEBUG = True

BASE_DIR = Path(__file__).resolve().parent

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

MEDIA_ROOT  = os.path.join(BASE_DIR, 'CookbookAPI/media')
MEDIA_URL = '/media/'
STATIC_ROOT  = os.path.join(BASE_DIR, 'CookbookAPI/static')
STATIC_URL = '/static/'
API_URL = 'http://127.0.0.1:8000'
```

# Deployment

In order to run the application on your webserver you need to create the necessary static files and migrations.
To do so please run the following code within the projects root directory:

```
python manage.py collectstatic
python manage.py generate_swagger -o swagger.json
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
