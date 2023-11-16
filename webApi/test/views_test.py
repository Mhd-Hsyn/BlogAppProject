from passlib.hash import django_pbkdf2_sha256 as handler
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from webApi.models import *


class UserSignup_TestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_Signup(self):
        url = reverse("userauth-signup")
        data = {
            "fname": "Syed",
            "lname": "Hussain",
            "email": "syd.mhd.hsyn@gmail.com",
            "password": "hussain123",
        }
        response = self.client.post(url, data, format="json")
        res_data = response.json()
        self.assertEqual(res_data['status'], True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        updated_user = User.objects.get(email =  "syd.mhd.hsyn@gmail.com")
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().fname, "Syed")
        self.assertEqual(User.objects.get().lname, "Hussain")
        self.assertEqual(User.objects.get().email, "syd.mhd.hsyn@gmail.com")
        self.assertTrue(handler.verify("hussain123", updated_user.password))


class UserLogin_TestCase(TestCase):
    def setUp(self) -> None:
        url = reverse("userauth-signup")
        data = {
            "fname": "Syed",
            "lname": "Hussain",
            "email": "syd.mhd.hsyn@gmail.com",
            "password": "hussain123",
        }
        self.client.post(url, data, format="json")
    
    def test_login (self):
        url = reverse("userauth-login")
        data = {
            "email": "syd.mhd.hsyn@gmail.com",
            "password": "hussain123",
        }
        response= self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data= response.data
        self.assertEqual(data['message'], "Login Successfully")
        # after successfull login test JWT token is stored in table or not
        fetch_user = User.objects.get(email = "syd.mhd.hsyn@gmail.com")
        self.assertEqual( UserJWTWhiteListToken.objects.filter(user_id = fetch_user).count(), 1)