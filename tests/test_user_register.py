import unittest
from http import HTTPStatus
from app import create_app
from extension import db


class FlaskAPITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global app
        app = create_app("testing")
        cls.app = app.test_client()
        with app.app_context():
            # db.drop_all()
            db.create_all()

    def test_case_1(self):
        """Tests for user registration"""
        data = {
                "username": "test_client",
                "email": "test_client@gmail.com",
                "password": "tester_client_password",
                "phone_number": "07000000000"
            }

        response = self.app.post("/users/register", json=data)
        # print(response.json)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertIn("access_token", response.json)

    def test_case_2(self):
        """Tests for existing username during user registration"""
        data = {
            "username": "test_client",
            "email": "test_client_1@yahoo.com",
            "password": "test_client_password",
            "phone_number": "07011111100"
        }
        response = self.app.post("/users/register", json=data)
        # print(response.json)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertDictEqual(response.json, {'message': 'username already exists'})

    def test_case_3(self):
        """Test for existing email address during user registration"""
        data = {
            "username": "test_client_1",
            "email": "test_client@gmail.com",
            "password": "test_client_1_password",
            "phone_number": "07011111100"
        }
        response = self.app.post("/users/register", json=data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertDictEqual(response.json, {"message": "email address already registered to a different user"})

    def test_case_4(self):
        """Test for existing phone_number during user registration"""
        data = {
            "username": "test_client_1",
            "email": "test_client_1@gmail.com",
            "password": "test_client_1_password",
            "phone_number": "07000000000"
        }
        response = self.app.post("/users/register", json=data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertDictEqual(response.json, {"message": "phone number already registered to a different user"})

    def test_case_5(self):
        """Test for JSON request validation"""
        data = {
            "username":"test_client_1"
        }
        response = self.app.post("/users/register", json=data)
        errors = response.json["errors"]
        self.assertEqual(errors["password"], ['Missing data for required field.'])
        self.assertEqual(errors["email"], ['Missing data for required field.'])
        self.assertEqual(errors["phone_number"], ['Missing data for required field.'])

    def test_case_6(self):
        response = self.app.get("/users/register")
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    # def test_case_7(self):
    #     data = {
    #         "username": "test_client",
    #         "password": "tester_client_password"
    #     }
    #     response = self.app.post("/login", json=data)
    #     self.assertEqual(response.status_code, HTTPStatus.OK)
    #     self.assertIn("access_token", response.json)
    #     self.access_token = response.json["access_token"]

    def test_case_7(self):
        data = {
            "email": "test_client",
            "password": "tester_client_password"
        }
        response = self.app.post("/login", json=data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)


    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.drop_all()

if __name__ == '__main__':
    unittest.main(verbosity=4)

