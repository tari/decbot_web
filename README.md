# Dependencies
All dependencies except Python itself may be installed from pypi.

 * Python >= 3.0
 * django >= 1.6
 * djangorestframework

`virtualenv` is recommended for installation of dependencies, but not necessary.

# Configuration
Be sure to edit `decbot_web/settings.py` with your database configuration as
necessary, and change the secret key. Run `manage.py syncdb` to create database
tables.

# Upgrading
If the db schema changed, good luck. Try `manage.py sqlall` to see what the app
expects things to look like.

# Deployment
Refer to the [Django documentation](https://docs.djangoproject.com/en/1.6/howto/deployment/)
for deployment methods. Sample configurations are included in the `config` directory.
