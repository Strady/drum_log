from tests.utils import FastApiTestCase
from db_models import User
from passlib.context import CryptContext


class TestCreateUser(FastApiTestCase):

    def test_user_creation(self):
        """
        Tests user creation. Checks returned data and User entry in DB
        """
        ### Setup ###

        email = 'someone@somewhere.com'
        username = 'someone'
        password = 'never guess'

        ### Run ###

        response = self.client.post(
            url='/users/',
            json={'email': email, 'username': username, 'password': password}
        )

        ### Assertions ###

        self.assertEqual(200, response.status_code)
        self.assertEqual(email, response.json()['email'])
        self.assertEqual(username, response.json()['username'])

        user = self.run_coro(User.get(id=response.json()['id']))
        self.assertEqual(username, user.username)
        self.assertEqual(email, user.email)
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.assertIs(pwd_context.verify(password, user.password_hash), True)
