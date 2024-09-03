import os


JENKINS = {
    "URL": "http://0.0.0.0:18080",
    "USERNAME": os.environ.get("JENKINS_USER", "root"),
    "PASSWORD": os.environ.get("JENKINS_PASSWORD", "password"),
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SESSION_USER = "user"
DEBUG = True
STATIC_URL = "/static/"
ALLOWED_HOSTS = ["*"]
ROOT_URLCONF = "dj_jenkins.urls"
SECRET_KEY = "1234567890poiuytrewq"
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "django.contrib.sessions",
    "drf_yasg",
    "rest_framework",
    "dj_jenkins",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "jenkins",
        "USER": os.getenv("MYSQL_ROOT_USER", "root"),
        "PASSWORD": os.getenv("MYSQL_ROOT_PASSWORD", "password"),
        "HOST": os.getenv("MYSQL_HOST", "dj-mysql"),
        "PORT": os.getenv("MYSQL_PORT", 13306),
        "OPTIONS": {
            "init_command": "SET foreign_key_checks = 0;",
        }
    },
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]

REST_FRAMEWORK = {
    # define rdf api doc
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
}

