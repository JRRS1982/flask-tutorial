# https: // flask.palletsprojects.com/en/1.1.x/tutorial/tests/

import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
# tempfile.mkstemp creates a temp file returning the object and path to it, therefore overwriting the path to the database below. 
  db_fd, db_path = tempfile.mkstemp()

  app = create_app({
# tells flask that the app is in test mode. 
    'TESTING': True, 
# setting the path for the database... for the temp file. 
    'DATABASE': db_path,
  })

  with app.app_context():
    init_db()
    get_db().executescript(_data_sql)

    yield app
    
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
# tests will use the client test app above to make requests without running the server. 
  return app.test_client()

@pytest.fixture
def runner(app):
# similar to client above, this creates a runner that can call the client commands regisered with the applicaiton, so wont run the server. 
  return app.test_cli_runner()

