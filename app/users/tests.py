from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from .models import User


URL_SIGNUP = reverse('signup')
URL_LOGIN = reverse('login')


class BaseUserTestCase(APITestCase):

    def setUp(self):
        self.email = 'test@test.com'
        self.password = 'testpass'
        self.user = self.create_user(email=self.email, password=self.password)
        self.token = self.user.token
        self.api = self.create_authenticated_api_client(self.user.token)

    def create_user(self, email, password, is_superuser=False):
        user = User.objects.create(email=email, is_superuser=is_superuser)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user

    def create_authenticated_api_client(self, token):
        api = APIClient()
        api.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        return api


class UserCreationTests(APITestCase):

    def test_create_valid_user(self):
        """
        Create valid user
        """
        payload = {
            'email': 'foo@bar.com',
            'password': '12456',
        }
        api = APIClient()
        response = api.post(URL_SIGNUP, payload, format='json')
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', data)
        self.assertNotEqual('token', '')

    def test_create_user_requires_email(self):
        """
        Create a new user requires email
        """
        payload = {}
        api = APIClient()
        response = api.post(URL_SIGNUP, payload, format='json')
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', data)
        self.assertEqual(data['email'], ['This field is required.'])

    def test_create_user_requires_password(self):
        """
        Create a new user requires password
        """
        payload = {
            'email': 'foo@bar.com',
        }
        api = APIClient()
        response = api.post(URL_SIGNUP, payload, format='json')
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', data)
        self.assertEqual(data['password'], ['This field is required.'])

    def test_create_duplicated_user(self):
        """
        Create duplicated user
        """
        payload = {
            'email': 'foo@bar.com',
            'password': '12456',
        }
        api = APIClient()
        response = api.post(URL_SIGNUP, payload, format='json')
        response = api.post(URL_SIGNUP, payload, format='json')
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', data)
        self.assertEqual(data['email'], ['User with this email address already exists.'])


class UserLoginTests(BaseUserTestCase):

    def test_login_existing_user(self):
        """
        Login existing user
        """
        api = APIClient()
        payload = {
            'username': self.email,
            'password': self.password,
        }
        response = api.post(URL_LOGIN, payload, format='json')
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', data)
        self.assertNotEqual('token', '')

    def test_login_existing_user_invalid(self):
        """
        Login existing invalid user
        """
        api = APIClient()
        payload = {
            'username': self.email,
            'password': 'foo',
        }
        response = api.post(URL_LOGIN, payload, format='json')
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', data)
        self.assertIn('non_field_errors', data)
        self.assertEqual(data['non_field_errors'], ['Unable to log in with provided credentials.'])

    def test_login_unexisting_user(self):
        """
        Login unexisting user
        """
        api = APIClient()
        payload = {
            'username': 'foo',
            'password': 'foo',
        }
        response = api.post(URL_LOGIN, payload, format='json')
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', data)
        self.assertIn('non_field_errors', data)
        self.assertEqual(data['non_field_errors'], ['Unable to log in with provided credentials.'])


class UserRetrievalTests(BaseUserTestCase):

    def test_user_profile(self):
        """
        Retrieve user profile
        """
        url = reverse('users-list')
        response = self.api.get(url, format='json')
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('email', data)
        self.assertIn('first_name', data)
        self.assertIn('last_name', data)
        self.assertIn('created', data)
        self.assertNotIn('password', data)
        self.assertEqual(data['email'], self.user.email)

    def test_user_profile_detail(self):
        """
        Retrieve user profile detail
        """
        url = reverse('users-detail', args=[str(self.user.pk)])
        response = self.api.get(url, format='json')
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('email', data)
        self.assertIn('first_name', data)
        self.assertIn('last_name', data)
        self.assertIn('created', data)
        self.assertNotIn('password', data)
        self.assertEqual(data['email'], self.user.email)

    def test_user_profile_different_id(self):
        """
        Retrieve user profile with different id
        """
        user = self.create_user('foo@bar.com', 'foobar')
        api = self.create_authenticated_api_client(user.token)
        url = reverse('users-detail', args=[str(user.pk)])
        response = api.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.api.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserUpdateTests(BaseUserTestCase):

    def test_update_existing_user(self):
        """
        Update an existing user.
        """
        url = reverse('users-detail', args=[str(self.user.pk)])
        payload = {
            'first_name': 'first-name',
            'last_name': 'last-name',
        }
        response = self.api.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'first-name')
        self.assertEqual(response.data['last_name'], 'last-name')

    def test_update_unexisting_user(self):
        """
        Tries to update a non-existing user.
        """
        url = reverse('users-detail', args=['unexistent-uuid'])
        response = self.api.put(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_existing_user(self):
        """
        Partial update an existing user.
        """
        url = reverse('users-detail', args=[str(self.user.pk)])
        payload = {
            'first_name': 'partial',
        }
        response = self.api.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'partial')
        self.assertEqual(response.data['last_name'], self.user.last_name)

    def test_partial_update_unexisting_user(self):
        """
        Tries to update an non-existing user.
        """
        url = reverse('users-detail', args=['unexistent-uuid'])
        response = self.api.patch(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_avoid_updating_user_email(self):
        """
        Update an existing user but make sure that email field is not changed.
        """
        url = reverse('users-detail', args=[str(self.user.pk)])
        payload = {
            'email': 'xxx@yyy.zzz',
        }
        response = self.api.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_avoid_user_updating_other_user(self):
        """
        Update an existing user but make sure that email field is not changed.
        """
        user = self.create_user('foo@bar.com', 'foobar')
        url = reverse('users-detail', args=[str(user.pk)])
        payload = {
            'first_name': 'foo',
            'last_name': 'bar',
        }
        response = self.api.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_avoid_user_partial_updating_other_user(self):
        """
        Update an existing user but make sure that email field is not changed.
        """
        user = self.create_user('foo@bar.com', 'foobar')
        url = reverse('users-detail', args=[str(user.pk)])
        payload = {
            'first_name': 'foo',
        }
        response = self.api.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserDeleteTests(BaseUserTestCase):

    def test_user_delete(self):
        """
        Disallow user delete
        """
        url = reverse('users-detail', args=[str(self.user.pk)])
        response = self.api.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)