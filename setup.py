#!/usr/bin/env python

from setuptools import setup, find_packages
DESCRIPTION = ('OAuth2 Provider for Flask applications.')
with open('README.rst') as f:
    LONG_DESCRIPTION = f.read()

install_requires = [
    'Flask-OAuthlib',
    'Flask-PyMongo',
    'bcrypt',
    'pyOpenSSL',
    'redis',
]


setup(
    name='Flask-Sentinel',
    version='0.0.4',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author='Nicola Iarocci',
    author_email='nicola@nicolaiarocci.com',
    url='https://github.com/nicolaiarocci/flask-sentinel',
    license='BSD',
    platforms=["any"],
    packages=find_packages(),
    package_data={'flask_sentinel': ['templates/*']},
    test_suite="flask.ext.sentinel.tests",
    install_requires=install_requires,
    tests_require=['redis'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
