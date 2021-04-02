from django.test import TestCase
from django.contrib.auth.models import User
from . models import Profile
# Create your tests here.
class TestModels(TestCase):

    def setUp(self):
        user2 = User.objects.create_user(
            first_name = "Tsering" ,
            last_name = "Sherpa",
            username = "tsedik25",
            email = "tsering@gmail.com",
            password = "tsering123",
        )

    def test_create_profile(self):
        user = User.objects.get(username = "tsedik25")
        pro = Profile.objects.get(user = user)
        print(pro)