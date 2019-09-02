import pytest
from flask import g, session
from flaskr.db import get_db

def test_register(client, app):
# client.get() makes a GET request and returns the Response object, returned by flask. 
# to test that the page reders cuccessfully a simple request is made and checked for a 200 OK status_code, if it is unsuccessful there would be a 500 Internal Server Error code.
  assert client.get('auth/register').status_code == 200
  response = client.post(
    '/auth/register', data={'username': 'a', 'password': 'a'}
  )
  # headers will have a Location header with the login URL when the register view redirects to the login view. 
  assert 'http://localhost/auth/login' == response.headers['Location']

  with app.app_context():
    assert get_db().execute(
      "select * from user where username = 'a'",
    ).fetchone() is not None
#pytest.mark.parametrize tells Pytest to run the same test fucntions with different arguments. You use it here to test difference invalid input and error messages without writing the same code three times. i..e username, passwors and message are being checked here - i think. 
@pytest.mark.parametrize(('username', 'password', 'message'), (
  ('', '', b'Username is required.'),
  ('a', '', b'Password is required'.),
  ('test', 'test', b'already registered'),
))


def test_register_validate_input(client, username, password, message):
# similar to the GET requesat above client.post() makes a POST request converting the data dict into form data. 
  response = client.post(
    '/auth/register',
    # data contains teh body of the response as bytes. If you expect a certain value to render on the page check that its in data. Bytes must be compared to bytes, if you want to compare Unicode text, use get_data(as_text=True) instead.
    data={'username': username, 'password': password}
  )
  assert message in response.data

def test_login(client, auth):
  assert client.get('/auth/login').status_code == 200
  response = auth.login()
  assert response.headers['Location'] == 'http://localhost/'

# using client in a WITH block allows accessing context variables such as session after the response is returned. Normally accessing session outside of a request would raise an error.
  with client:
    client.get('/')
    assert session['user_id'] == 1
    assert g.user['username'] == 'test'

@pytest.mark.paramertize(('username', 'password', 'message'), (
  ('a', 'test', b'Incorrect username'),
  ('test', 'a', b'Incorrect password.'),
))

def test_login_validate_input(auth, username, password, message):
  response = auth.login(username, password)
  assert message in response.data


# testing logout is clearly the opposite of login, the session should not contain user_id after logging out as it is cleared during that process.
def test_logout(client, auth):
  auth.login()

  with client:
    auth.logout()
    assert 'user_id' not in session