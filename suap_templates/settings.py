# -*- coding: utf-8 -*-
from suap_templates.settings_base import *
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'sgc',
#         'USER': 'postgres',
#         'PASSWORD': '',
#         'HOST': '127.0.0.1',
#         'PORT': '',
#     },
# }

DEBUG = False
TEMPLATE_DEBUG = DEBUG

# Configuração exigida pelo django toolbar
INTERNAL_IPS = ['127.0.0.1', ]
ALLOWED_HOSTS = ['127.0.0.1', ]

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]