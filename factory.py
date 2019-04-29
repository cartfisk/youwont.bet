# -*- coding: utf-8 -*-
"""
app.factory
~~~~~~~~~~~
Create the WSGI application.
:copyright: (c) 2016 by Benjamin Bertrand.
:license: BSD 2-Clause, see LICENSE for more details.
"""
from flask import Flask
import settings
from views import api


def create_app():
    application = Flask(__name__)
    application.config.from_object(settings)
    application.config.from_envvar('LOCAL_SETTINGS', silent=True)
    application.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
    application.register_blueprint(api)
    return application
