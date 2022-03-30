import asyncio
import os
from fastapi.testclient import TestClient
from unittest import TestCase
from tortoise.contrib.test import initializer, finalizer
from passlib.hash import bcrypt
import db_models

os.environ['JWT_SECRET'] = 'something'
os.environ['API_KEY'] = 'some_key'

from settings import AppSettings
from main import app

app_config = AppSettings()


class FastApiTestCase(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)
        cls.client.headers.update({app_config.api_key_header: os.environ['API_KEY']})
        initializer(['db_models'])

    @classmethod
    def tearDownClass(cls) -> None:
        finalizer()

    @staticmethod
    def run_coro(coro):
        return asyncio.get_event_loop().run_until_complete(coro)

    @staticmethod
    async def create_user(email: str, username: str, password):
        return await db_models.User.create(
            email=email,
            username=username,
            password_hash=bcrypt.hash(password)
        )
