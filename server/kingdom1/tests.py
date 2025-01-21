import unittest
from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import jwt

from main import create_access_token, verify_token, SECRET_KEY, ALGORITHM


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

if __name__ == "__main__":
    unittest.main()
