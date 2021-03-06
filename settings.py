# Universal Subtitles, universalsubtitles.org
# 
# Copyright (C) 2010 Participatory Culture Foundation
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see 
# http://www.gnu.org/licenses/agpl-3.0.html.

# Django settings for mirosubs project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'mirosubs.sqlite3'    # Or path to database file if using sqlite3.
DATABASE_USER = ''                    # Not used with sqlite3.
DATABASE_PASSWORD = ''                # Not used with sqlite3.
DATABASE_HOST = ''                    # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''                    # Set to empty string for default. Not used with sqlite3.

JS_USE_COMPILED = False

# paths provided relative to media/js
JS_RAW = ['mirosubs.js', 
          'rpc.js',
          'abstractvideoplayer.js',
          'html5videoplayer.js',
          'youtubevideoplayer.js',
          'html5videosource.js',
          'youtubevideosource.js',
          'unitofwork.js', 
          'clippy.js',
          'flash.js',
          'spinner.js',
          'widget/videotab.js',
          'widget/dialog.js',
          'widget/captionmanager.js',
          'widget/mainmenu.js',
          'widget/rightpanel.js',
          'widget/subtitle/dialog.js',
          'widget/subtitle/msservermodel.js',
          'widget/subtitle/editablecaption.js',
          'widget/subtitle/subtitlewidget.js',
          'widget/subtitle/subtitlelist.js',
          'widget/subtitle/transcribeentry.js',
          'widget/subtitle/transcribepanel.js',
          'widget/subtitle/transcriberightpanel.js',
          'widget/subtitle/syncpanel.js',
          'widget/subtitle/reviewpanel.js',
          'widget/subtitle/finishedrightpanel.js',
          'widget/translate/dialog.js',
          'widget/translate/translationpanel.js',
          'widget/translate/translationlist.js',
          'widget/translate/translationwidget.js',
          'widget/translate/editabletranslation.js',
          'widget/translate/servermodel.js',
          'widget/play/manager.js',
          'widget/embeddablewidget.js']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')+'/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site_media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'a9yr_yzp2vmj-2q1zq)d2+b^w(7fqu2o&jh18u9dozjbd@-$0!'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'openid_consumer.middleware.OpenIDMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
   os.path.join(os.path.dirname(__file__),'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'context_processors.current_site',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'socialauth',
    'openid_consumer',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django_extensions',
    'profiles',
    'sorl.thumbnail',
    'videos',
    'widget',
    'auth',
    'south'
)

AUTH_PROFILE_MODULE = 'profiles.Profile'
ACCOUNT_ACTIVATION_DAYS = 9999 # we are using registration only to verify emails
SESSION_COOKIE_AGE = 2419200 # 4 weeks

RECENT_ACTIVITIES_ONPAGE = 10

FEEDBACK_EMAIL = 'feedback@universalsubtitles.org'
FEEDBACK_SUBJECT = 'Feedback'
