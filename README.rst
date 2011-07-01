=======
Djobberbase
=======

Djobberbase is an easy to use Django app that allows developers to have a job board in a django site. It replicates almost 100% the functionalities of the jobberBase php software (`http://www.jobberbase.com <http://www.djangoproject.com/>`_).


********
Requirements:
********

* Python 2.7+ 
* Django 1.2.4+ (may work on 1.3 but untested!)

********
Optional requirements:
********

* ``django-simple-captcha`` (for captchas)
* ``textile`` (for markup)
* ``markdown`` (for markup)


************
Installation
************


To install Djobberbase:

1. ``pip install django-djobberbase``
2. Add ``'djobberbase'`` to your `INSTALLED_APPS` in ``settings.py``
3. Add an URL entry for ``djobberbase`` in ``urls.py``::
    

        urlpatterns = patterns('',
            (r'^myjobsite/', include('djobberbase.urls')),
        )
