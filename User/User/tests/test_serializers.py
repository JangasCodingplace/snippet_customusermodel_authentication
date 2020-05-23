from django.contrib import auth

from django.test import TestCase

from rest_framework.authtoken.models import Token
from User.User.models import User
from User.User.serializers import (
    BaseUserSerializer,
    UserSerializer,
    AuthUserSerializer
)

class BaseUserSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name='Test',
            last_name='User',
            email='test@user.com',
            password='testpassword1'
        )
    
    def test_serializer_response(self):
        user_serializer = BaseUserSerializer(self.user)
        expected_response = {
            'first_name':'Test',
            'last_name':'User',
            'email':'test@user.com',
            'is_active':True,
            'auth_token':Token.objects.get(user=self.user).key
        }

        self.assertDictEqual(user_serializer.data,expected_response)
    
    def test_serializer_valid_creation(self):
        test_data = {
            'first_name':'Test',
            'last_name':'User',
            'email':'test@serializer.com',
            'password':'testpassword1'
        }

        user_serializer = BaseUserSerializer(data=test_data)
        if user_serializer.is_valid(raise_exception=True):
            new_user = user_serializer.save()
        
        expected_response = {
            'first_name':'Test',
            'last_name':'User',
            'email':'test@serializer.com',
            'is_active':True,
            'auth_token':Token.objects.get(user=new_user).key
        }

        self.assertDictEqual(user_serializer.data,expected_response)

        user_obj = User.objects.get(email=test_data['email'])
        self.assertEqual(new_user,user_obj)

    def test_serializer_not_valid_by_missing_first_name(self):
        test_data = {
            'last_name':'INVALID_DATA',
            'email':'invalid@mail.com',
            'password':'pwForInvalidData'
        }
        user_serializer = BaseUserSerializer(data=test_data)
        self.assertFalse(user_serializer.is_valid())
    
    def test_serializer_not_valid_by_missing_last_name(self):
        test_data = {
            'first_name':'INVALID_DATA',
            'email':'invalid@mail.com',
            'password':'pwForInvalidData'
        }
        user_serializer = BaseUserSerializer(data=test_data)
        self.assertFalse(user_serializer.is_valid())

    def test_serializer_not_valid_by_missing_email(self):
        test_data = {
            'first_name':'INVALID_DATA',
            'last_name':'INVALID_DATA',
            'password':'pwForInvalidData'
        }
        user_serializer = BaseUserSerializer(data=test_data)
        self.assertFalse(user_serializer.is_valid())

    def test_serializer_not_valid_by_missing_password(self):
        test_data = {
            'first_name':'INVALID_DATA',
            'last_name':'INVALID_DATA',
            'email':'invalid@mail.com',
        }
        user_serializer = BaseUserSerializer(data=test_data)
        self.assertFalse(user_serializer.is_valid())

class UserSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name='Test',
            last_name='User',
            email='test@user.com',
            password='testpassword1'
        )

    def test_serializer_response(self):
        user_serializer = UserSerializer(self.user)
        expected_response = {
            'first_name':'Test',
            'last_name':'User',
            'email':'test@user.com',
            'is_active':True
        }

        self.assertDictEqual(user_serializer.data,expected_response)
    
    def test_update_all(self):
        """
        Note: The UserModels should be functional for this case!
        """
        user = User.objects.create_user(
            first_name='Test',
            last_name='User',
            email='test1@user.com',
            password='testpassword1'
        )

        user_backup_first_name = user.first_name
        user_backup_last_name = user.last_name

        change_data = {
            'first_name':'ChangeTestFirstName',
            'last_name':'ChangeTestLastName',
        }

        user_serializer = UserSerializer(user, data=change_data)
        if user_serializer.is_valid(raise_exception=True):
            edited_user = user_serializer.save()
        
        expected_response = {
            'first_name':'ChangeTestFirstName',
            'last_name':'ChangeTestLastName',
            'email':'test1@user.com',
            'is_active':True
        }

        self.assertDictEqual(user_serializer.data, expected_response)

        self.assertNotEqual(user.first_name,user_backup_first_name)
        self.assertNotEqual(user.last_name,user_backup_last_name)
    
    def test_update_first_name(self):
        """
        Note: The UserModels should be functional for this case!
        """
        user = User.objects.create_user(
            first_name='Test',
            last_name='User',
            email='test2@user.com',
            password='testpassword1'
        )

        user_backup_first_name = user.first_name
        user_backup_last_name = user.last_name

        change_data = {
            'first_name':'ChangeTestFirstName',
        }

        user_serializer = UserSerializer(user, data=change_data)
        if user_serializer.is_valid(raise_exception=True):
            edited_user = user_serializer.save()
        
        expected_response = {
            'first_name':'ChangeTestFirstName',
            'last_name':'User',
            'email':'test2@user.com',
            'is_active':True
        }

        self.assertDictEqual(user_serializer.data, expected_response)

        self.assertNotEqual(user.first_name,user_backup_first_name)

    def test_update_last_name(self):
        """
        Note: The UserModels should be functional for this case!
        """
        user = User.objects.create_user(
            first_name='Test',
            last_name='User',
            email='test3@user.com',
            password='testpassword1'
        )

        user_backup_last_name = user.last_name

        change_data = {
            'last_name':'ChangeTestLastName',
        }

        user_serializer = UserSerializer(user, data=change_data)
        if user_serializer.is_valid(raise_exception=True):
            edited_user = user_serializer.save()
        
        expected_response = {
            'first_name':'Test',
            'last_name':'ChangeTestLastName',
            'email':'test3@user.com',
            'is_active':True
        }

        self.assertDictEqual(user_serializer.data, expected_response)
        self.assertNotEqual(user.last_name,user_backup_last_name)

    def test_update_without_data(self):
        data = {}

        first_name_backup = self.user.first_name
        last_name_backup = self.user.last_name

        user_serializer = UserSerializer(self.user, data=data)
        self.assertTrue(user_serializer.is_valid())

        if user_serializer.is_valid(raise_exception=True):
            updated_user = user_serializer.save()
        
        self.assertTrue(updated_user.first_name, first_name_backup)
        self.assertTrue(updated_user.last_name, last_name_backup)


class AuthUserSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name='Test',
            last_name='User',
            email='test@user.com',
            password='testpassword1'
        )

    def test_serializer_response(self):
        user_serializer = UserSerializer(self.user)
        expected_response = {
            'first_name':'Test',
            'last_name':'User',
            'email':'test@user.com',
            'is_active':True
        }

        self.assertDictEqual(user_serializer.data,expected_response)
    
    def test_update_all(self):
        """
        Note: The UserModels should be functional for this case!
        """
        user = User.objects.create_user(
            first_name='Test',
            last_name='User',
            email='test1@user.com',
            password='testpassword1'
        )

        user_backup_email = user.email
        

        change_data = {
            'email':'testX@user.com',
            'password':'newPassword',
        }

        user_serializer = AuthUserSerializer(user, data=change_data)
        if user_serializer.is_valid(raise_exception=True):
            edited_user = user_serializer.save()
        
        expected_response = {
            'first_name':'Test',
            'last_name':'User',
            'email':'testX@user.com',
            'is_active':True
        }

        self.assertDictEqual(user_serializer.data, expected_response)
        self.assertNotEqual(user.email,user_backup_email)

        successfull_login = auth.authenticate(
            email=user.email,
            password=change_data['password']
        )
        self.assertIsNotNone(successfull_login)

        not_successfull_login_1 = auth.authenticate(
            email=user.email,
            password='testpassword1'
        )

        self.assertIsNone(not_successfull_login_1)

        not_successfull_login_2 = auth.authenticate(
            email=user_backup_email,
            password='testpassword1'
        )

        self.assertIsNone(not_successfull_login_2)

        not_successfull_login_3 = auth.authenticate(
            email=user_backup_email,
            password=change_data['password']
        )

        self.assertIsNone(not_successfull_login_3)

    def test_update_email(self):
        """
        Note: The UserModels should be functional for this case!
        """
        user = User.objects.create_user(
            first_name='Test',
            last_name='User',
            email='test2@user.com',
            password='testpassword1'
        )

        user_backup_email = user.email
        
        change_data = {
            'email':'testX@user.com',
        }

        user_serializer = AuthUserSerializer(user, data=change_data)
        if user_serializer.is_valid(raise_exception=True):
            edited_user = user_serializer.save()
        
        expected_response = {
            'first_name':'Test',
            'last_name':'User',
            'email':'testX@user.com',
            'is_active':True
        }

        self.assertDictEqual(user_serializer.data, expected_response)
        self.assertNotEqual(user.email,user_backup_email)

        successfull_login = auth.authenticate(
            email=user.email,
            password='testpassword1'
        )
        self.assertIsNotNone(successfull_login)

        not_successfull_login_1 = auth.authenticate(
            email=user_backup_email,
            password='testpassword1'
        )

        self.assertIsNone(not_successfull_login_1)

    def test_update_password(self):
        """
        Note: The UserModels should be functional for this case!
        """
        user = User.objects.create_user(
            first_name='Test',
            last_name='User',
            email='test3@user.com',
            password='testpassword1'
        )

        change_data = {
            'password':'newPassword',
        }

        user_serializer = AuthUserSerializer(user, data=change_data)
        if user_serializer.is_valid(raise_exception=True):
            edited_user = user_serializer.save()
        
        expected_response = {
            'first_name':'Test',
            'last_name':'User',
            'email':'test3@user.com',
            'is_active':True
        }

        self.assertDictEqual(user_serializer.data, expected_response)

        successfull_login = auth.authenticate(
            email=user.email,
            password=change_data['password']
        )
        self.assertIsNotNone(successfull_login)

        not_successfull_login_1 = auth.authenticate(
            email=user.email,
            password='testpassword1'
        )

        self.assertIsNone(not_successfull_login_1)

    def test_update_without_data(self):
        data = {}

        password_backup = 'testpassword1'
        email_backup = self.user.email

        user_serializer = UserSerializer(self.user, data=data)
        self.assertTrue(user_serializer.is_valid())

        if user_serializer.is_valid(raise_exception=True):
            updated_user = user_serializer.save()
        
        self.assertTrue(updated_user.email, email_backup)

        successfull_login = auth.authenticate(
            email=email_backup,
            password=password_backup
        )

        self.assertIsNotNone(successfull_login)

        