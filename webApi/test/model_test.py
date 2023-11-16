from django.test import TestCase
from webApi.models import *


class AdminModel_TestCase(TestCase):
    def setUp(self):
        self.user = User(
            fname="Muhammad",
            lname="Hussain",
            email="syd.mhd.hsyn@gmail.com",
            password="hussain123",
        )

    def test_admin_create(self):
        self.user.save()
        fetch_user = User.objects.get(email="syd.mhd.hsyn@gmail.com")
        self.assertEqual(fetch_user.fname, "Muhammad")
        self.assertEqual(fetch_user.lname, "Hussain")
        self.assertEqual(fetch_user.email, "syd.mhd.hsyn@gmail.com")
        self.assertEqual(fetch_user.password, "hussain123")

    def test_admin_str(self):
        self.assertEqual(str(self.user), "syd.mhd.hsyn@gmail.com")


class Category_TestCase(TestCase):
    def setUp(self) -> None:
        self.category = Category(
            name = "Software",
            description= "Software Technology releted post"
        )
    
    def test_CategoryCreate(self):
        self.category.save()
        fetch_cat = Category.objects.get(name = "Software")
        self.assertEqual(fetch_cat.name, "Software")
        self.assertEqual(fetch_cat.description, "Software Technology releted post")
