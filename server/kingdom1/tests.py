import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from passlib.hash import bcrypt

from fastapi import HTTPException
from jose import jwt
from main import (
    create_access_token,
    verify_token,
    SECRET_KEY,
    ALGORITHM,
    app,
)
from fastapi.testclient import TestClient

client = TestClient(app)


class TestJWTUtils(unittest.TestCase):

    def setUp(self):
        self.test_data = {"sub": "testuser"}
        self.invalid_token = jwt.encode({"sub": "invaliduser"}, "wrongkey", algorithm=ALGORITHM)

    def test_create_access_token(self):
        token = create_access_token(self.test_data)
        self.assertIsInstance(token, str)
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        self.assertEqual(decoded["sub"], self.test_data["sub"])

    def test_create_access_token_with_expiration(self):
        expires_delta = timedelta(minutes=10)
        token = create_access_token(self.test_data, expires_delta)
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp = datetime.utcfromtimestamp(decoded["exp"])
        self.assertGreater(exp, datetime.utcnow())

    def test_verify_valid_token(self):
        token = create_access_token(self.test_data)
        username = verify_token(token)
        self.assertEqual(username, self.test_data["sub"])

    def test_verify_invalid_token(self):
        with self.assertRaises(HTTPException) as cm:
            verify_token(self.invalid_token)
        self.assertEqual(cm.exception.status_code, 403)
        self.assertEqual(cm.exception.detail, "Could not validate credentials")

    def test_verify_expired_token(self):
        expires_delta = timedelta(seconds=-1)
        token = create_access_token(self.test_data, expires_delta)
        with self.assertRaises(HTTPException) as cm:
            verify_token(token)
        self.assertEqual(cm.exception.status_code, 403)
        self.assertEqual(cm.exception.detail, "Could not validate credentials")

class TestAPIEndpoints(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    @patch("main.get_db_connection")
    def test_register_user(self, mock_db_conn):
        mock_cursor = MagicMock()
        mock_db_conn.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {"id": 1}

        response = self.client.post("/register", json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "securepassword"
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("User registered successfully", response.json()["message"])


    @patch("main.get_db_connection")
    def test_create_subscription_plan(self, mock_db_conn):
        mock_cursor = MagicMock()
        mock_db_conn.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {"id": 1}

        response = self.client.post("/subscriptions/plans", json={
            "name": "Premium Plan",
            "price": 10.99,
            "duration_days": 30,
            "description": "Access to premium features"
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn("Subscription plan created successfully", response.json()["message"])

    @patch("main.get_db_connection")
    def test_incorrect_login(self, mock_db_conn):
        mock_cursor = MagicMock()
        mock_db_conn.return_value.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = {
            "id": 1,
            "username": "testuser",
            "password_hash": bcrypt.hash("securepassword")
        }

        response = self.client.post("/login", json={
            "username": "testuser",
            "password": "wrongpassword"
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid username or password", response.json()["detail"])

    @patch("main.get_db_connection")
    def test_correct_login(self, mock_db_conn):
        mock_cursor = MagicMock()
        mock_db_conn.return_value.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = {
            "id": 1,
            "username": "testuser",
            "password_hash": bcrypt.hash("securepassword")
        }

        response = self.client.post("/login", json={
            "username": "testuser",
            "password": "securepassword"
        })

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())
        self.assertEqual(response.json()["token_type"], "bearer")


if __name__ == "__main__":
    unittest.main()
