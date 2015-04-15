# Dependencies
All dependencies except Python itself may be installed from pypi.

 * Python >= 2.7 (>= 3.0 is OK)
 * django >= 1.6
 * djangorestframework

`virtualenv` is recommended for installation of dependencies, but not necessary.

# Configuration
Be sure to edit `decbot_web/settings.py` with your database configuration as
necessary, and change the secret key.

Database setup scripts are provided in the `sql` directory. Execute them on
your database in numerical order and everything *should* be okay. You may need
to modify the scripts slightly depending on what database engine you use.

# Upgrading

If there's a new database schema revision, the requisite update script will be
provided in the `sql` directory. Run the new SQL script(s) on your database
and everything should be taken care of. Backups are recommended before
attempting any upgrade, though.

# Deployment
Refer to the [Django documentation](https://docs.djangoproject.com/en/1.6/howto/deployment/)
for deployment methods. Sample configurations are included in the `config` directory.
