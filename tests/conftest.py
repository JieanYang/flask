import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
	_data_sql = f.read().decode('urf8')


@pytest.fixture
def app():
	# db_fd is a temporary file object, db_path is the temporary file path
	db_fd, db_path = tempfile.mkstemp()

	app = create_app({
		'TESTING': True, 
		'DATABASE': db_path	
	})

	with app.app_context():
		# Create database
		init_db()
		# Insert data
		get_db().executescript(_data_sql)

	yield app

	# The temporary file will close and remove after the whole test
	os.close(db_fd)
	os.unlink(db_path)

# Tests will use the client to make requests to the application without running the server
@pytest.fixture
def client(app):
	return app.test_client()

# Create a runner that can call the Click commands registered with the application
@pytest.fixture
def runner(app):
	return app.test_cli_runner()


class AuthAction(object):
	def __init__(self, client):
		self._client = client

	def login(self, username='test', password='test'):
		return self._client.post(
			'/auth/login', 
			data={'username': username, 'password': password}
		)

	def logout(self):
		return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
	return AuthAction(client)

