#!/usr/bin/env python

from setuptools import setup, find_packages
DESCRIPTION = ('OAuth2 Provider powered by Flask, Redis and MongoDB.')
with open('README.md') as f:
    LONG_DESCRIPTION = f.read()

install_requires = [
    'Flask-OAuthlib',
    'Flask-PyMongo',
    'bcrypt',
    'pyOpenSSL',
    'redis',
]

setup(
    name='Gateman',
    version='0.0.1',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author='Nicola Iarocci',
    author_email='gateman@nicolaiarocci.com',
    url='https://github.com/nicolaiarocci/gateman',
    license='BSD',
    platforms=["any"],
    packages=find_packages(),
    test_suite="gateman.tests",
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
