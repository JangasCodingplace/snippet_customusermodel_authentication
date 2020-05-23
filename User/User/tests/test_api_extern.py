import json

from rest_framework.test import APITestCase

from rest_framework.authtoken.models import Token
from User.User.models import User

class LoginTest(APITestCase):
    """
    Note: Cookie Tests are missing yet!
    """
    def setUp(self):
        self.user = User.objects.create_user(
            first_name='Test',
            last_name='User',
            email='test@user.com',
            password='testpassword1'
        )
    
    def test_succesfull_login_by_email(self):
        path = '/user/auth/login'
        data = {
            'email':'test@user.com',
            'password':'testpassword1',
        }
        response = self.client.post(path, data)
        expected_response = {'user':{
                'first_name':self.user.first_name,
                'last_name':self.user.last_name,
                'email':self.user.email,
                'is_active':self.user.is_active,
                'auth_token':Token.objects.get(user=self.user).key
            }
        }
        self.assertDictEqual(expected_response, response.json())
    
    def test_not_succesfull_login_by_email_wrong_password(self):
        path = '/user/auth/login'
        data = {
            'email':'test@user.com',
            'password':'testpassword2',
        }
        response = self.client.post(path, data)
        expected_response = {
            'err':'User does not exist or wrong password.'
        }
        
        self.assertDictEqual(expected_response, response.json())

    def test_not_succesfull_login_by_email_wrong_email(self):
        path = '/user/auth/login'
        data = {
            'email':'testX@user.com',
            'password':'testpassword1',
        }
        response = self.client.post(path, data)
        expected_response = {
            'err':'User does not exist or wrong password.'
        }
        
        self.assertDictEqual(expected_response, response.json())

    def test_invalid_login_request_missing_email(self):
        path = '/user/auth/login'
        data = {
            'password':'testpassword1',
        }
        response = self.client.post(path, data)
        expected_response = {
            'err':'Missing request data'
        }
        
        self.assertDictEqual(expected_response, response.json())
    
    def test_invalid_login_request_missing_password(self):
        path = '/user/auth/login'
        data = {
            'email':'test@user.com',
        }
        response = self.client.post(path, data)
        expected_response = {
            'err':'Missing request data'
        }
        
        self.assertDictEqual(expected_response, response.json())


class CreateUserTest(APITestCase):
    """
    Note: Cookie Tests are missing yet!
    """
    def test_successfull_creation(self):
        path = '/user/auth/create_user'
        data = {
            'first_name':'Test',
            'last_name':'User',
            'email':'test@user.com',
            'password':'testpassword1',
        }
        response = self.client.post(path, data)

        user = User.objects.get(email=data['email'])
        token = Token.objects.get(user=user).key

        expected_response = {
            'user':{
                'first_name':user.first_name,
                'last_name':user.last_name,
                'email':user.email,
                'is_active':user.is_active,
                'auth_token':token
            }
        }
        self.assertDictEqual(expected_response, response.json())

    def test_failed_creation_by_recreate_user(self):
        u = User.objects.create_user(
            first_name = 'Test',
            last_name = 'User',
            email = 'nodouble@test.com',
            password = 'testpassword1'
        )

        path = '/user/auth/create_user'
        data = {
            'first_name':'Test',
            'last_name':'User',
            'email':'nodouble@test.com',
            'password':'testpassword1'
        }

        response = self.client.post(path, data)

        expected_response = {
            'err':'User with that Email does already exist.'
        }

        self.assertDictEqual(expected_response, response.json())

    def test_failed_creation_by_missing_data_first_name(self):
        path = '/user/auth/create_user'
        data = {
            'last_name':'User',
            'email':'nodouble@test.com',
            'password':'testpassword1'
        }

        response = self.client.post(path, data)

        expected_response = {
            'err':'Missing request data'
        }

        self.assertDictEqual(expected_response, response.json())

    def test_failed_creation_by_missing_data_last_name(self):
        path = '/user/auth/create_user'
        data = {
            'first_name':'Test',
            'email':'nodouble@test.com',
            'password':'testpassword1'
        }

        response = self.client.post(path, data)

        expected_response = {
            'err':'Missing request data'
        }

        self.assertDictEqual(expected_response, response.json())

    def test_failed_creation_by_missing_data_email(self):
        path = '/user/auth/create_user'
        data = {
            'first_name':'Test',
            'last_name':'User',
            'password':'testpassword1'
        }

        response = self.client.post(path, data)

        expected_response = {
            'err':'Missing request data'
        }

        self.assertDictEqual(expected_response, response.json())

    def test_failed_creation_by_missing_data_password(self):
        path = '/user/auth/create_user'
        data = {
            'first_name':'Test',
            'last_name':'User',
            'email':'nodouble@test.com',
        }

        response = self.client.post(path, data)

        expected_response = {
            'err':'Missing request data'
        }

        self.assertDictEqual(expected_response, response.json())
