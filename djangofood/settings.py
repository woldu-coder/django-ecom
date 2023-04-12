from pathlib import Path
import os
import dj_database_url
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-dtu27rqmqm73#6dk$w%rrnnqoij%&%e2pf8sm4fjs#2ih8-#8$"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["delish-delivery.onrender.com"]


# Application definition

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    # My Apps
    "delivery.apps.DeliveryConfig",
    
    # Third part modules
    "rest_framework",
    "crispy_bootstrap5",
    "crispy_forms",
    "corsheaders",
    "whitenoise",
]
CRISPY_TEMPLATE_PACK="bootstrap5"
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # Django middle ware
    "whitenoise.middleware.WhiteNoiseMiddleware",
    
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "djangofood.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "djangofood.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "djangofood",
#         "USER": "postgres",
#         "PASSWORD": "post@wako12",
#         "HOST": "localhost",
#         "PORT": "5432",
#     }
# }
DATABASES={
    "default": dj_database_url.parse("postgres://delivery_4rtw_user:S1CZSbA88BksTuqEVUk1ZH4gSwoejrLr@dpg-cgr4r4e4dadccqrbqm70-a.frankfurt-postgres.render.com/delivery_4rtw")
}
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS=[
    os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = "/images/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
# EMAIL_HOST_USER=os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD='zoetczzmjzbhdumo'
EMAIL_HOST_USER='woldugizaw7@gmail.com'
# EMAIL_HOST_PASSWORD='odaefexdqzexkeqa'

AUTH_USER_MODEL="delivery.User"
# Allowing others to access
CORS_ALLOW_ALL_ORIGINS=True

JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Admin",

    "site_header": "Delish",
    "site_brand": "Delish",

    "login_logo": None,

    # Logo to use for login form in dark themes (defaults to login_logo)
    "login_logo_dark": None,

    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle",

    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,

    # Welcome text on the login screen
    "welcome_sign": "Welcome to the library",

    # Copyright on the footer
    "copyright": "Delish Delivery Ltd",
    "search_model": ["auth.User", "auth.Group"],

    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,
    "topmenu_links": [
        # {"name": "Home",  "url": "http://127.0.0.1:8000/admin/", "permissions": ["auth.view_user"]},
        {"name": "Users",  "url": "#", "permissions": ["auth.view_user"]},
        {"name": "Groups",  "url": "#", "permissions": ["auth.view_user"]},
        {"name": "Add Hotel",  "url": "#", "permissions": ["auth.view_user"]},
        {"name": "Add Food",  "url": "#", "permissions": ["auth.view_user"]},
        
    ],

   "usermenu_links": [
        {"name": "facebook", "url": "https://facebook.com/auth.user/", "new_window": True},
        {"name": "twitter", "url": "https://twitter.com/auth.user/", "new_window": True},
        {"model": "auth.user"}
    ],

    
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True,

    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],

    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    "related_modal_active": False,

    "custom_css": None,
    "custom_js": None,
    # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
    "use_google_fonts_cdn": True,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,

    "changeform_format": "horizontal_tabs",
    "language_chooser": False,
}