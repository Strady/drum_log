import datetime
import os
from jose import jwt
from tests.utils import FastApiTestCase


class TestAuthentication(FastApiTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super(TestAuthentication, cls).setUpClass()
        cls.email = 'someone@somewhere.com'
        cls.username = 'someone'
        cls.password = 'never guess'
        cls.user = cls.run_coro(cls.create_user(email=cls.email, username=cls.username, password=cls.password))

    def test_successful_authentication(self):
        """
        Tests authentication for existing user with correct credentials
        """
        ### Setup ###

        ### Run ###

        response = self.client.post(
            url='/auth/login',
            data={'username': self.email, 'password': self.password}
        )

        ### Assertions ###

        self.assertEqual(200, response.status_code)
        self.assertEqual('bearer', response.json()['token_type'])

        payload = jwt.decode(response.json()['access_token'], os.environ['JWT_SECRET'], algorithms=['HS256'])
        self.assertEqual(self.user.id, int(payload['sub']))
        self.assertGreater(payload['exp'], datetime.datetime.utcnow().timestamp())

    def test_not_existing_user(self):
        """
        Tests authentication attempt for not registered user
        """
        ### Setup ###

        email = 'wrong@mail.com'
        ### Run ###

        response = self.client.post(
            url='/auth/login',
            data={'username': email, 'password': self.password}
        )

        ### Assertions ###

        self.assertEqual(401, response.status_code)
        self.assertEqual(f'{{"detail":"User with {email} email is not registered"}}', response.text)

    def test_incorrect_password(self):
        """
        Tests authentication attempt with incorrect password
        """
        ### Run ###

        response = self.client.post(
            url='/auth/login',
            data={'username': self.email, 'password': 'some password'}
        )

        ### Assertions ###

        self.assertEqual(401, response.status_code)
        self.assertEqual('{"detail":"Password is incorrect"}', response.text)



