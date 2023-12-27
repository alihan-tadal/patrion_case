from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Factory


class FactoryUserTests(TestCase):
    """Test Factory User"""

    def setUp(self):
        self.client = APIClient()
        self.ru = get_user_model().objects.create_user(
            email="ru@test.com",
            password="testpass",
            name="Test Factory User",
            surname="Surname",
        )
        self.ru2 = get_user_model().objects.create_user(
            email="ru2@test.com",
            password="testpass",
            name="Test Factory User 2",
            surname="Surname 2",
        )
        self.client.force_authenticate(self.ru)

    def test_list_factory_success(self):
        """Test listing factory"""
        f1 = Factory.objects.create(
            name="Test Factory",
            address="Test Address",
            city="Test City",
            country="Test Country",
        )
        self.ru.factory = f1
        self.ru.save()

        res = self.client.get(reverse("factory:list"))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_list_factory_success_just_their_factories(self):
        """Test listing factory"""
        f1 = Factory.objects.create(
            name="Test Factory",
            address="Test Address",
            city="Test City",
            country="Test Country",
        )
        self.ru.factory = f1
        self.ru.save()
        f2 = Factory.objects.create(
            name="Test Factory 2",
            address="Test Address 2",
            city="Test City 2",
            country="Test Country 2",
        )
        self.ru2.factory = f2
        self.ru.save()
        res = self.client.get(reverse("factory:list"))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_ru_cannot_create_factory(self):
        """Test that RU cannot create factory"""
        payload = {
            "name": "Test Factory",
            "address": "Test Address",
            "city": "Test City",
            "country": "Test Country",
        }
        res = self.client.post(reverse("factory:create"), payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_ru_update_factory(self):
        """Test that RU can update factory"""
        factory = Factory.objects.create(
            name="Test Factory",
            address="Test Address",
            city="Test City",
            country="Test Country",
        )
        self.ru.factory = factory
        self.ru.save()
        payload = {
            "name": "Test Factory Updated",
            "address": "Test Address Updated",
            "city": "Test City Updated",
            "country": "Test Country Updated",
        }
        res = self.client.patch(
            reverse("factory:update", kwargs={"pk": factory.pk}), payload
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        factory.refresh_from_db()
        self.assertEqual(factory.name, payload["name"])
        self.assertEqual(factory.address, payload["address"])
        self.assertEqual(factory.city, payload["city"])
        self.assertEqual(factory.country, payload["country"])

    def test_ru_cannot_delete_factory(self):
        """Test that RU cannot delete factory"""
        factory = Factory.objects.create(
            name="Test Factory",
            address="Test Address",
            city="Test City",
            country="Test Country",
        )
        self.ru.factory = factory
        self.ru.save()
        res = self.client.delete(reverse("factory:delete", kwargs={"pk": factory.pk}))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_ru_cannot_update_others_factory(self):
        """Test that RU cannot update others factory"""
        factory = Factory.objects.create(
            name="Test Factory",
            address="Test Address",
            city="Test City",
            country="Test Country",
        )
        self.ru2.factory = factory
        self.ru2.save()
        payload = {
            "name": "Test Factory Updated",
            "address": "Test Address Updated",
            "city": "Test City Updated",
            "country": "Test Country Updated",
        }
        res = self.client.patch(
            reverse("factory:update", kwargs={"pk": factory.pk}), payload
        )
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


class AdminUserTests(TestCase):
    """Test Admin User"""

    def setUp(self):
        self.client = APIClient()
        self.su = get_user_model().objects.create_superuser(
            email="su@test.com", password="testpass"
        )
        self.client.force_authenticate(self.su)

    def test_list_factory_success(self):
        """Test listing factory"""
        f1 = Factory.objects.create(
            name="Test Factory",
            address="Test Address",
            city="Test City",
            country="Test Country",
        )
        self.su.factory = f1
        self.su.save()
        f2 = Factory.objects.create(
            name="Test Factory 2",
            address="Test Address 2",
            city="Test City 2",
            country="Test Country 2",
        )
        self.su.factory = f2
        self.su.save()
        res = self.client.get(reverse("factory:list"))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_su_create_factory(self):
        """Test that SU can create factory"""
        payload = {
            "name": "Test Factory",
            "address": "Test Address",
            "city": "Test City",
            "country": "Test Country",
        }
        res = self.client.post(reverse("factory:create"), payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["name"], payload["name"])
        self.assertEqual(res.data["address"], payload["address"])
        self.assertEqual(res.data["city"], payload["city"])
        self.assertEqual(res.data["country"], payload["country"])

    def test_su_update_factory(self):
        """Test that SU can update factory"""
        factory = Factory.objects.create(
            name="Test Factory",
            address="Test Address",
            city="Test City",
            country="Test Country",
        )
        self.su.factory = factory
        self.su.save()
        payload = {
            "name": "Test Factory Updated",
            "address": "Test Address Updated",
            "city": "Test City Updated",
            "country": "Test Country Updated",
        }
        res = self.client.patch(
            reverse("factory:update", kwargs={"pk": factory.pk}), payload
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        factory.refresh_from_db()
        self.assertEqual(factory.name, payload["name"])
        self.assertEqual(factory.address, payload["address"])
        self.assertEqual(factory.city, payload["city"])
        self.assertEqual(factory.country, payload["country"])

    def test_su_delete_factory(self):
        """Test that SU can delete factory"""
        factory = Factory.objects.create(
            name="Test Factory",
            address="Test Address",
            city="Test City",
            country="Test Country",
        )
        self.su.factory = factory
        self.su.save()
        res = self.client.delete(reverse("factory:delete", kwargs={"pk": factory.pk}))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_su_update_others_factory(self):
        """Test that SU can update others factory"""
        factory = Factory.objects.create(
            name="Test Factory",
            address="Test Address",
            city="Test City",
            country="Test Country",
        )
        self.su.factory = factory
        self.su.save()
        payload = {
            "name": "Test Factory Updated",
            "address": "Test Address Updated",
            "city": "Test City Updated",
            "country": "Test Country Updated",
        }
        res = self.client.patch(
            reverse("factory:update", kwargs={"pk": factory.pk}), payload
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        factory.refresh_from_db()
        self.assertEqual(factory.name, payload["name"])
        self.assertEqual(factory.address, payload["address"])
        self.assertEqual(factory.city, payload["city"])
        self.assertEqual(factory.country, payload["country"])

    def test_autogenerated_user_can_get_token(self):
        """Test that autogenerated user can get token"""
        # create a factory through api
        payload = {
            "name": "Test Factory",
            "address": "Test Address",
            "city": "Test City",
            "country": "Test Country",
        }
        res = self.client.post(reverse("factory:create"), payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # get token for the autogenerated user
        user_email = res.data.get("user_email")
        res = self.client.post(
            reverse("user:token_obtain_pair"),
            {"email": user_email, "password": "changeme"},
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)

    def test_user_count_doesnt_change_after_update_op(self):
        """Test that user count doesnt change after update op"""
        # create a factory through api
        payload = {
            "name": "Test Factory",
            "address": "Test Address",
            "city": "Test City",
            "country": "Test Country",
        }
        res = self.client.post(reverse("factory:create"), payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # get user count
        user_count = get_user_model().objects.count()
        # update the factory
        factory_id = res.data.get("id")
        payload = {
            "name": "Test Factory Updated",
            "address": "Test Address Updated",
            "city": "Test City Updated",
            "country": "Test Country Updated",
        }
        res = self.client.patch(
            reverse("factory:update", kwargs={"pk": factory_id}), payload
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # check the user count
        self.assertEqual(get_user_model().objects.count(), user_count)
