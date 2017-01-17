from flask import json, url_for
from .base import BaseTestCase


class TestAuth(BaseTestCase):

    def test_404(self):
        """Tests invalid url or non-existing route returns 404 error"""
        response = self.client.get(
            '/wrong/url',
        )
        self.assertEqual(response.status_code, 404)
        output = json.loads(response.data)
        self.assertEqual(output['error'], 'Resource not found.')

    def test_register_user_success(self):
        """Tests User is registered successfully"""
        response = self.client.post(url_for('api.register'), data=json.dumps({
            'username': 'createuser',
            'email': 'createuser@gmail.com',
            'password': 'test-password',
        }), content_type='application/json')

        self.assertEqual(response.status_code, 201)

        output = json.loads(response.data)
        self.assertIn(b'token', output)

    def test_register_with_same_email(self):
        """
        Tests that no two users cannot have the same email address.
        Note: email address should be a unique field in the database.
        """
        response = self.client.post(url_for('api.register'), data=json.dumps({
            'username': 'createuser2',
            'email': 'createuser@gmail.com',
            'password': 'test-password',
        }), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        output = json.loads(response.data)
        self.assertIn(b'error', output)

    def test_register_with_same_username(self):
        """
        Tests that no two users cannot have the same username.
        Note: username should be a unique field in the database.
        """
        response = self.client.post(url_for('api.register'), data=json.dumps({
            'username': 'createuser',
            'email': 'createuser2@gmail.com',
            'password': 'test-password',
        }), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        output = json.loads(response.data)
        self.assertIn(b'error', output)

    def test_user_login(self):
        """
        Tests user logs in successfully.
        """
        response = self.client.post(
            url_for('api.login'),
            data=json.dumps({
                'username': 'test',
                'password': 'test-password',
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data)
        self.assertIn(b'token', output)

    def test_invalid_login_credentials(self):
        """
        Tests loggin in with invalid credentials returns errors.
        tests that an error is returned when trying to log in with
        invalid password or no password.
        or with a non-existing username or when username is not provided.
        """

        # test with Invalid password
        response = self.client.post(url_for('api.login'), data=json.dumps({
            'username': 'test',
            'password': 'invalid-password',
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        output = json.loads(response.data)
        self.assertIn('error', output)

        # password not provided
        response = self.client.post(url_for('api.login'), data=json.dumps({
            'username': 'test',
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        output = json.loads(response.data)
        self.assertIn('error', output)

        # username not provided.
        response = self.client.post(url_for('api.login'), data=json.dumps({
            'password': 'test-password',
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        output = json.loads(response.data)
        self.assertIn('error', output)

        # Username does not exist
        response = self.client.post(url_for('api.login'), data=json.dumps({
            'username': 'fake-tester',
            'password': 'test-password',
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        output = json.loads(response.data)
        self.assertIn('error', output)
