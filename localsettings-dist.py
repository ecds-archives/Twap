# Local settings file.  This should NEVER be checked in.

# Django settings for twap project.
from os import path

# Get the directory of this file for relative dir paths.
# Django sets too many absolute paths.
BASE_DIR = path.dirname(path.abspath(__file__))

# FOR DEVELOPMENT ENVIRONMENTS AND TROUBLESHOOTING ONLY
# set these to True, otherwise leave them set to false.
DEV_ENV = True
DEBUG = True
TEMPLATE_DEBUG = True

ADMINS = (
        # Name and email address of people to email as admins.
        # 'Name', 'email@email.com'
            )

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': '', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Make this unique, and don't share it with anybody.
# You can grab one here https://www.grc.com/passwords.htm
SECRET_KEY = ''

# These are used to connect and read from the twitter streaming API

TWITTER_USER = '' 
TWITTER_PASSWORD = ''