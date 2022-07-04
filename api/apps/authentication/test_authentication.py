from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from api.apps.authentication.models import User


class AuthenticationAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test123@mail.com',
            password='test123')

# TODO: add more checks in methods
    def test_can_login(self):
        url = reverse('login')
        response = self.client.post(url, {'email': 'test123@mail.com', 'password': 'test123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_login_with_improper_password(self):
        url = reverse('login')
        response = self.client.post(url, {'email': 'test123@mail.com', 'password': 'some123'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_logout(self):
        url = reverse('logout')
        self.client.login(email='test123@mail.com', password='test123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_register(self):
        url = reverse('register')
        response = self.client.post(url, {'email': 'test2@mail.com', 'password': 'test222'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_change_password(self):
        url = reverse('reset-password')
        self.client.login(email='test123@mail.com', password='test123')
        response = self.client.patch(url, {'password': 'new_password'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
