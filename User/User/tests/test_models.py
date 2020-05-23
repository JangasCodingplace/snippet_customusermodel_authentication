from django.test import TestCase

from rest_framework.authtoken.models import Token
from User.User.models import User

from django.db.utils import IntegrityError

class StandardUserModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name='Test',
            last_name='User',
            email='test@user.com',
            password='testpassword1'
        )

    def test_user_first_name(self):
        self.assertEqual(self.user.first_name,'Test')

    def test_user_last_name(self):
        self.assertEqual(self.user.last_name,'User')

    def test_user_email(self):
        self.assertEqual(self.user.email,'test@user.com')
    
    def test_user_is_active(self):
        """
        Note: This test depends on your default settings if the User is active after first registration.
        Please chainge the expected value, when you changed the "is_active" settings. 
        """
        self.assertTrue(self.user.is_active)
    
    def test_user_is_not_superuser(self):
        self.assertFalse(self.user.is_admin)
    
    def test_registration_date_does_exist(self):
        self.assertNotEqual(self.user.registration_date,'')
        self.assertNotEqual(self.user.registration_date,None)

    def test_activation_date_does_exists(self):
        """
        Note: This test depends on your default settings if the User is active after first registration.
        If a user gets activated with registration, this value should always be set
        """
        self.assertNotEqual(self.user.activation_date,'')
        self.assertNotEqual(self.user.activation_date,None)

    def test_token_does_exists(self):
        try:
            token = Token.objects.get(user=self.user)
            self.assertTrue(True)
        except Token.DoesNotExist:
            self.assertTrue(False)
    
    def test_invalid_registration_by_missing_first_name(self):
        with self.assertRaises(TypeError):
            User.objects.create_user(
                last_name='Invalid',
                email='invalid@email.com',
                password='InvalidPW'
            )

    def test_invalid_registration_by_missing_last_name(self):
        with self.assertRaises(TypeError):
            User.objects.create_user(
                first_name='Invalid',
                email='invalid@email.com',
                password='InvalidPW'
            )

    def test_invalid_registration_by_missing_email(self):
        with self.assertRaises(TypeError):
            User.objects.create_user(
                first_name='Invalid',
                last_name='Invalid',
                password='InvalidPW'
            )
    
    def test_invalid_registration_by_missing_password(self):
        with self.assertRaises(AttributeError):
            User.objects.create_user(
                first_name='Invalid',
                last_name='Invalid',
                email='invalid@email.com'
            )

    def test_invalid_registration_by_invalid_password(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                first_name='Invalid',
                last_name='Invalid',
                email='invalid@email.com',
                password='invalid'
            )

    def test_user_is_already_taken(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                first_name='Invalid',
                last_name='Invalid',
                email='test@user.com',
                password='testpassword1'
            )


class SuperuserModelTests(TestCase):
    """
    Please Note: The Standard-Usermodel Tests above should be successful!
    In this test only admin specific Attributes and requirements gets test.
    """
    def setUp(self):
        self.user = User.objects.create_superuser(
            first_name='Test',
            last_name='User',
            email='admin@user.com',
            password='testpassword1'
        )

    def test_user_is_active(self):
        self.assertTrue(self.user.is_active)

    def test_activation_date_does_exists(self):
        self.assertNotEqual(self.user.activation_date,'')
        self.assertNotEqual(self.user.activation_date,None)
    
    def test_user_is_admin(self):
        self.assertTrue(self.user.is_admin)
