from setuptools import setup, find_packages

setup(
    name = "decbot_web",
    version = "0.2",
    author = "Peter Marheine",
    author_email = "peter@taricorp.net",
    description = ("A Django-based web interface to DecBot."),
    license = "BSD",
    packages = find_packages(),
    scripts = ['manage.py'],

    install_requires = [
        'django ==3.1',
        'djangorestframework >=3.0',
        'django-filter <2.0',
        'django-pipeline',
        'matplotlib'
    ]
)
