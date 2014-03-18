from setuptools import setup, find_packages

setup(
    name = "decbot_web",
    version = "0.2",
    author = "Peter Marheine",
    author_email = "peter@taricorp.net",
    description = ("A Django-based web interface to DecBot.")
    license = "BSD",
    packages = find_packages(),
    scripts = ['manage.py']

    install_requires = [
        'django',
        'djangorestframework',
        'django-filter',
        'matplotlib'
    ]
