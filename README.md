# Djobberbase

Djobberbase is an easy to use Django app that allows developers to have a job board in a django site. It replicates almost 100% the functionalities of the jobberBase php software [http://www.jobberbase.com](http://www.jobberbase.com/).

## Demo:

[Job board](http://derelict.mx/demo1/)

[Admin](http://derelict.mx/admin/)
  User: **demo**
  Password: **demo**

_Database is reset every hour._    


## Requirements:

* Python 2.7+
* Django 1.2.4+


# Djobberbase QuickStart Guide


## Getting Djobberbase


For the latest released version of Djobberbase you can get it with **pip** like this:

    pip install django-djobberbase

Alternatively, you can checkout the development version from GitHub (don't forget to put it in your PYTHONPATH!):django-simple-captcha, Markdown and textile.

    git clone https://github.com/wtrevino/django-djobberbase.git


## Optional requirements

Djobberbase can use 3 optional requirements:

* `django-simple-captcha` (for captchas)
* `textile` (for markup)
* `markdown` (for markup)

You can use a requirements file packed with Djobberbase to install all 3:

    pip install -r optional-requirements.txt

Notes: django-simple-captcha requires a recent version of PIL compiled with FreeType support. You can read more about django-simple-captcha configuration [here](http://code.google.com/p/django-simple-captcha/wiki/CaptchaConfiguration).

You can switch between or use Markdown and textile alternatively for markup capabilities in the job application form as well as the job posting form.


## Installation


To install Djobberbase into your project just add it in your INSTALLED_APPS. If you also want django-simple-captcha you need to add it as well:

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',

        # Uncomment the next line to enable the admin:
        'django.contrib.admin',

        # third party
        'djobberbase',
        'captcha',
    )

You can now synchronize with the database:

    python manage.py syncdb

Djobberbase comes with a default set of templates, if you want to use them on a **development environment** you need to make sure the media (css, js, images) that comes with it is served. To do this you can use the STATICFILES_DIR tuple in your project's settings.py (Django 1.3+).

    import djobberbase

    DJOBBERBASE_ROOT = os.path.dirname(os.path.realpath(djobberbase.__file__))

    STATICFILES_DIRS = (    
        ("css", os.path.join(DJOBBERBASE_ROOT, 'media/css')),
        ("img", os.path.join(DJOBBERBASE_ROOT, 'media/img')),
        ("js", os.path.join(DJOBBERBASE_ROOT, 'media/js')),
    )  

Also make sure you use the `python manage.py collectstatic` command on your project so it can collect the media files to your static folder.

## Configuration

Make sure you add `djobberbase.context_processors.general_settings` to your project's template processors in settings.py, **remember not to override Django's default template context processors**.:

    TEMPLATE_CONTEXT_PROCESSORS = (
        "django.contrib.auth.context_processors.auth",
        "django.core.context_processors.debug",
        "django.core.context_processors.i18n",
        "django.core.context_processors.media",
        "django.core.context_processors.static",
        "django.core.context_processors.tz",
        "django.contrib.messages.context_processors.messages",
        "djobberbase.context_processors.general_settings"
    )

In order to make use of email notifications you need to configure Django email settings in settings.py:

    EMAIL_HOST = 'smtp.mydomain.com'
    EMAIL_HOST_USER = 'mailbox_username'
    EMAIL_HOST_PASSWORD = 'mailbox_password'
    DEFAULT_FROM_EMAIL = 'valid_email_address'
    SERVER_EMAIL = 'valid_email_address'

    #Djobberbase specific
    DJOBBERBASE_ADMIN_EMAIL = DEFAULT_FROM_EMAIL
    DJOBBERBASE_FILE_UPLOADS = MEDIA_ROOT

Activate notifications:

    DJOBBERBASE_ADMIN_NOTIFICATIONS = True
    DJOBBERBASE_POSTER_NOTIFICATIONS = True
    DJOBBERBASE_APPLICATION_NOTIFICATIONS = True

Activate form captchas for posts and/or applications, (optional, you can only use `'simple'` for now):

    DJOBBERBASE_CAPTCHA_APPLICATION = 'simple'
    DJOBBERBASE_CAPTCHA_POST = 'simple'

If you do use django-simple-captcha you need to add an entry to your urls.py:

    urlpatterns += patterns('',
        url(r'^captcha/', include('captcha.urls')),
    )

Activate markup for job posts (optional, you can use either `'textile'` or `'markdown'`):

    DJOBBERBASE_MARKUP_LANGUAGE = 'textile'


Congratulations! Your Djobberbase site is now ready.

For a complete list of (a lot!) more configuration elements please check the [Djobberbase-Configuration](https://github.com/wtrevino/django-djobberbase/wiki/Djobberbase-Configuration) wiki page.
