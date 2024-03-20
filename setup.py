from os import environ

from setuptools import setup
from datetime import datetime

version = environ.get('VERSION', datetime.now().strftime('%Y%m%d%H%M%S'))

setup(
    name='godaddy-dns-updater',
    description='DNS Updater for GoDaddy with support for multiple subdomains.',
    author='Pieter-Jan Vrielynck',
    # Date-based versioning (YYYYMMDDHHMMSS)
    version=version,
    packages=['godaddydnsupdater'],
    install_requires=[
        'configloader==1.0.1',
        'GoDaddyPy==2.5.1',
        'pyYAML==6.0.1',
        'ratelimit==2.2.1'],
)