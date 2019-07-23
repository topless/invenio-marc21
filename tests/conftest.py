# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Pytest configuration."""

from __future__ import absolute_import, print_function

import os

import pytest
from flask import Flask
from flask_babelex import Babel
from invenio_db import InvenioDB, db
from invenio_indexer import InvenioIndexer
from invenio_jsonschemas import InvenioJSONSchemas
from invenio_records import InvenioRecords
from invenio_search import InvenioSearch, current_search

from invenio_marc21 import InvenioMARC21


@pytest.fixture()
def app():
    """Flask application fixture."""
    app = Flask('testapp')
    app.config.update(
        JSONSCHEMAS_ENDPOINT='/',
        JSONSCHEMAS_HOST='http://localhost:5000',
        INDEXER_DEFAULT_INDEX='',
        SEARCH_INDEX_PREFIX='test-',
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            'SQLALCHEMY_DATABASE_URI', 'sqlite:///test.db'),
    )

    Babel(app)
    if not hasattr(app, 'cli'):
        from flask_cli import FlaskCLI
        FlaskCLI(app)
    InvenioDB(app)
    InvenioRecords(app)
    InvenioMARC21(app)
    InvenioSearch(app)
    InvenioIndexer(app)
    InvenioJSONSchemas(app)
    return app


@pytest.fixture()
def es(app):
    """Flask application with records fixture."""
    with app.app_context():
        db.create_all()
        list(current_search.create(ignore=None))

    yield current_search

    with app.app_context():
        db.drop_all()
        list(current_search.delete())
