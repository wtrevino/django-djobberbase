# -*- coding: utf-8 -*-

from distutils.core import setup
setup(
    name = "django-djobberbase",
    packages = [
            "djobberbase",
            "djobberbase.conf",
            "djobberbase.templatetags",
    ],
    package_data = {       
        'djobberbase': [
            'templates/djobberbase/emails/*.txt',
            'templates/djobberbase/emails/*.html',
            'templates/djobberbase/*.html',
            'locale/es/LC_MESSAGES/django.mo',
            'locale/es/LC_MESSAGES/django.po',
            'media/css/*.css',
            'media/img/*.gif',
            'media/img/*.png',
            'media/js/*.js'
        ],
    },
    version="0.1.1",
    license="MIT",
    description = "A clone of the jobberBase job board platform written using the Django framework.",
    author = "Walter Treviño",
    author_email = "wtrevino@derelict.mx",
    url = "https://github.com/wtrevino/django-djobberbase",
    keywords = ["django", "python", "jobberbase", "job board"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ],
)

