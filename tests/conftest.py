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


# for most of the views a user neds to be logged in, the easiest way of doing that in tests is to make a POST request to teh login view with the client. Rather than writing that out every time, you can write a class with methods to do that, and use a fixture to pass it the client for each test.

#  with the auth fixture you can call auth.login() in a test to log in as the test user, which was inserted as part of the test data in teh app fixture. The register view should render successfully on GET. On POST with valid form data, it shoudl redirect to the login URL and the users data should be in the database. Invalid data should display error messages. 

# so i think that this acts as a form of helper method to log in a user for tests... speciifcally the authentication tests. 
class AuthActions(object):
  def __init__(self, client):
    self._client - client
  
  def login(self, username='test', password='test'):
    return self._client.post(
      '/auth/login',
      data={'username': username, 'password': password}
    )

  def logout(self):
    return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
  return AuthActions(client)
