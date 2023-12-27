from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient




"""
urlpatterns = [

    ## All Users
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("detail/", views.RetrieveUserView.as_view(), name="me"),

    ## Admin User
    path("create/", views.CreateUserView.as_view(), name="create"),
    path("detail/<int:pk>/", views.RetrieveUserByIdView.as_view(),  name="detail"),
    path("update/<int:pk>/", views.UpdateUserByIdView.as_view(), name="update"),
    path("delete/<int:pk>/", views.DeleteUserByIdView.as_view(), name="delete"),
    path("list/", views.ListUserView.as_view(), name="list"),
]


"""


CREATE_USER_URL = reverse("user:create")


class UserTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.payload = {
            "email": "test@test.com",
            "password": "testpass",
            "name": "Test name",
            "surname": "Test surname",
        }

        self.client = APIClient()
        self.su = get_user_model().objects.create_superuser(
            email="su@test.com", password="superuser"
        )
        self.ru = get_user_model().objects.create_user(
            email="ru@test.com", password="regularuser", name="Regular", surname="User"
        )

        self.client.force_authenticate(self.su)

    def test_su_create_user(self):
        """Test creating user with superuser"""

        payload = self.payload
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_ru_cannot_create_user(self):
        """Test creating user with regular user"""

        payload = self.payload
        self.client.logout()
        self.client.force_authenticate(self.ru)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_exists(self):
        """Test creating user that already exists"""
        payload = self.payload
        get_user_model().objects.create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_create(self):
        """Test that token is created for user"""
        payload = self.payload
        get_user_model().objects.create_user(**payload)
        res = self.client.post(reverse("user:token_obtain_pair"), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)



class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.payload = {
            "email": "test@test.com",
            "password": "testpass",
            "name": "Test name",
            "surname": "Test surname",
        }

        self.client = APIClient()
        self.su = get_user_model().objects.create_superuser(
            email="su@test.com", password="superuser"
        )
        self.ru = get_user_model().objects.create_user(
            email="ru@test.com", password="regularuser", name="Regular", surname="User"
        )

        self.client.force_authenticate(self.su)

    def test_retrieve_user(self):
        """Test retrieving profile for logged in user"""
        res = self.client.get(reverse("user:me"))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("email", res.data)

    def test_retrieve_user_by_id(self):
        """Test retrieving user by id"""
        res = self.client.get(reverse("user:detail", kwargs={"pk": self.ru.pk}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("email", res.data)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        self.client.logout()
        res = self.client.get(reverse("user:me"))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_su_create_user(self):
        """Test creating user with superuser"""

        payload = self.payload
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_ru_create_user(self):
        """Test creating user with regular user"""

        payload = self.payload
        self.client.logout()
        self.client.force_authenticate(self.ru)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_cannot_create_superuser(self):
        """Test creating superuser with regular user"""

        payload = {
            "email": "testsu@test.com",
            "password": "testpass",
            "name": "Test name",
            "surname": "Test surname",
            "is_superuser": True,
        }
        self.client.logout()
        self.client.force_authenticate(self.ru)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

            
