import pytest
from flask import g, session
from flaskr.db import get_db


# register
def test_register(client, app):
	assert client.get('/auth/register').status_code == 200
	# Make a post request
	response = client.post(
		'/auth/register', data={'username': 'a', 'password': 'a'}
	)

	# data contains the body of the response as bytes. If you expect a certain value to render on the page, check that it’s in data. Bytes must be compared to bytes. If you want to compare Unicode text, use get_data(as_text=True) instead.

	# Check url
	assert 'http://localhost/auth/login' == response.headers['Location']

	with app.app_context():
		assert get_db().execute(
			"Select * from user where username = 'a'", 
		).fetchone() is not None

# pytest.mark.parametrize tells Pytest to run the same test function with different arguments.
@pytest.mark.parametrize(('username', 'password', 'message'), (
	('', '', b'Username is requried.'), 
	('a', '', b'Password is required.'), 
	('test', 'test', b'already registered'), 
))
def test_register_validate_input(client, username, password, message):
	response = client.post(
		'/auth/register', 
		data={'username': username, 'password': password}
	)
	assert messsage in response.data


# login
def test_login(client, auth):
	assert client.get('/auth/login').status_code = 200
	response = auth.login()
	assert response.headers['Location'] == 'http://localhost/'

	# Using client in a with block allows accessing context variables such as session after the response is returned.
	with client:
		client.get('/')
		assert session['user_id'] = 1
		assert g.user['username'] == 'test'

@pytest.mark.parametrize(('username', 'password', 'message'), (
	('a', 'test', b'Incorrect username.'), 
	('test', 'a', b'Incorrect password'), 
))
def test_login_valide_input(auth, username, password, message):
	response = auth.login(username, password)
	assert message in response.data


# logout
def test_logout(client, auth):
	auth.login()

	# Using client in a with block allows accessing context variables such as session after the response is returned.
	with client:
		auth.logout()
		assert 'user_id' not in session