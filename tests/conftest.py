import pytest
import os
import subprocess

os.getenv('DB_NAME', 'vlan_config_test_db')
os.getenv('DB_PASSWORD', 'vlan_config_test_db_password')
os.getenv('DB_USER', 'vlan_config_test_db_user')

import db

os.environ['TEST_DB'] = db.db_uri

from app import create_app

@pytest.fixture()
def app():
    app = create_app()

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

@pytest.fixture(autouse=True)
def fake_db():
    engine = db.engine
    connection = engine.connect()
    subprocess.run(['alembic', 'upgrade', 'head'])

    session = db.Session()

    yield session

    session.rollback()
    subprocess.run(['alembic', 'downgrade', 'base'])
    connection.close()

    session.close()
