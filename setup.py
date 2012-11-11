# -*- coding: utf-8 -*-

from distutils.core import setup
setup(
    name = "django-simpleads,
    packages = [
            "simpleads,
            "simpleadsconf",
            "simpleadstemplatetags",
    ],
    package_data = {       
        'simpleads: [
            'templates/simpleadsemails/*.txt',
            'templates/simpleadsemails/*.html',
            'templates/simpleads*.html',
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
    author_email = "walter.trevino@gmail.com",
    url = "https://github.com/wtrevino/django-simpleads,
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

