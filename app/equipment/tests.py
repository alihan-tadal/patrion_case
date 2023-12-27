# import uuid
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient


from core.models import Factory, Equipment
from equipment.serializers import EquipmentSerializer


CREATE_EQUIPMENT_URL = reverse("equipment:create")
UPDATE_EQUIPMENT_URL = reverse("equipment:update", args=[1])
DELETE_EQUIPMENT_URL = reverse("equipment:delete", args=[1])
LIST_EQUIPMENT_BY_FACTORY_ID_URL = reverse("equipment:list", args=[1])


class PublicEquipmentAPITests(TestCase):
    """Test the publicly available equipment API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving equipment"""
        res = self.client.get(LIST_EQUIPMENT_BY_FACTORY_ID_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateEquipmentAPITests(TestCase):
    """Test the authorized user equipment API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="ru@test.com",
            password="testpass",
        )

        self.factory = Factory.objects.create(
            name="Factory 1",
            address="Factory 1 address",
            city="Factory 1 city",
            country="Factory 1 country",
        )
        self.user.factory = self.factory
        self.user.save()
        self.equipment = Equipment.objects.create(
            factory=self.factory,
            name="Equipment 1",
            description="Equipment 1 description",
            price=100.00,
            date="2021-01-01",
            status=True,
        )

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_setup(self):
        """Test that setup is correct"""
        self.assertEqual(self.user.email, "ru@test.com")
        self.assertEqual(self.factory.name, "Factory 1")
        self.assertEqual(self.equipment.name, "Equipment 1")

        # check relationship
        self.assertEqual(self.factory.equipments.first().name, "Equipment 1")
        self.assertEqual(self.equipment.factory.name, "Factory 1")
        self.assertEqual(self.user.factory.name, "Factory 1")

    def test_list_equipment_by_factory_id(self):
        """Test retrieving a list of equipment"""
        res = self.client.get(
            LIST_EQUIPMENT_BY_FACTORY_ID_URL, args=[self.user.factory.id]
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_other_factory_users_cannot_list_equipment(self):
        """Test that other factory users cannot list equipment"""

        # create another factory
        factory2 = Factory.objects.create(
            name="Factory 2",
            address="Factory 2 address",
            city="Factory 2 city",
            country="Factory 2 country",
        )
        # create a equipment in factory2
        equipment2 = Equipment.objects.create(
            factory=factory2,
            name="Equipment 2",
            description="Equipment 2 description",
            price=100.00,
            date="2021-01-01",
            status=True,
        )
        # create a user for factory2
        user2 = get_user_model().objects.create_user(
            email="ru2@test.com",
            password="testpass",
        )
        user2.is_staff = False
        user2.factory = factory2
        user2.save()

        # logout current user
        self.client.logout()
        self.client.force_authenticate(user2)

        # try to list equipment in factory1
        res = self.client.get(
            LIST_EQUIPMENT_BY_FACTORY_ID_URL, args=[self.user.factory.id]
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_equipment_successful(self):
        """Test creating a new equipment"""
        payload = {
            "name": "Equipment 2",
            # "factory": self.factory.id,
            "description": "Equipment 2 description",
            "price": 200.00,
            "date": "2021-01-01",
            "status": True,
        }
        res = self.client.post(CREATE_EQUIPMENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        equipment = Equipment.objects.get(id=res.data["id"])
        self.assertEqual(payload["name"], equipment.name)
        self.assertEqual(payload["description"], equipment.description)
        self.assertEqual(payload["price"], equipment.price)

    def test_update_equipment_successful(self):
        """Test updating an equipment"""
        payload = {
            "name": "Equipment 2",
            "factory": self.factory.id,
            "description": "Equipment 2 description",
            "price": 200.00,
            "date": "2021-01-01",
            "status": True,
        }
        res = self.client.put(UPDATE_EQUIPMENT_URL, payload, args=[self.equipment.id])
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        equipment = Equipment.objects.get(id=res.data["id"])
        self.assertEqual(payload["name"], equipment.name)
        self.assertEqual(payload["description"], equipment.description)
        self.assertEqual(payload["price"], equipment.price)

    def test_delete_equipment_successful(self):
        """Test deleting an equipment"""
        res = self.client.delete(DELETE_EQUIPMENT_URL, args=[self.equipment.id])
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        equipment = Equipment.objects.filter(id=self.equipment.id)
        self.assertEqual(len(equipment), 0)

    def test_other_factory_users_cannot_update_equipment(self):
        """Test that other factory users cannot update equipment"""

        # create another factory
        factory2 = Factory.objects.create(
            name="Factory 2",
            address="Factory 2 address",
            city="Factory 2 city",
            country="Factory 2 country",
        )
        # create a user for factory2
        user2 = get_user_model().objects.create_user(
            email="ru2@test.com",
            password="testpass",
        )
        user2.is_staff = False
        user2.factory = factory2
        user2.save()

        # logout current user
        self.client.logout()
        self.client.force_authenticate(user2)

        # try to update equipment in factory1
        payload = {
            "name": "Equipment 2",
            "factory": self.factory.id,
            "description": "Equipment 2 description",
            "price": 200.00,
            "date": "2021-01-01",
            "status": True,
        }
        res = self.client.put(UPDATE_EQUIPMENT_URL, payload, args=[self.equipment.id])
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_other_factory_users_cannot_delete_equipment(self):
        """Test that other factory users cannot delete equipment"""

        # create another factory
        factory2 = Factory.objects.create(
            name="Factory 2",
            address="Factory 2 address",
            city="Factory 2 city",
            country="Factory 2 country",
        )
        # create a user for factory2
        user2 = get_user_model().objects.create_user(
            email="ru2@test.com",
            password="testpass",
        )

        user2.is_staff = False
        user2.factory = factory2
        user2.save()

        # logout current user
        self.client.logout()
        self.client.force_authenticate(user2)

        # try to delete equipment in factory1
        res = self.client.delete(DELETE_EQUIPMENT_URL, args=[self.equipment.id])
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PropertyAPITests(TestCase):
    """Test the authorized user property API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="ru@test.com",
            password="testpass",
        )

        self.factory = Factory.objects.create(
            name="Factory 1",
            address="Factory 1 address",
            city="Factory 1 city",
            country="Factory 1 country",
        )

        self.user.factory = self.factory
        self.user.save()

        self.equipment = Equipment.objects.create(
            factory=self.factory,
            name="Equipment 1",
            description="Equipment 1 description",
            price=100.00,
            date="2021-01-01",
            status=True,
        )

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_create_property_successful(self):
        """Test creating a new property"""
        payload = {
            "name": "Property 1",
            "description": "Property 1 description",
            "equipment": self.equipment.id,
        }
        res = self.client.post(
            reverse("equipment:create_property", args=[self.equipment.id]), payload
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        eq = Equipment.objects.get(id=res.data["id"])
        self.assertEqual(payload["name"], eq.property_set.first().name)
        self.assertEqual(payload["description"], eq.property_set.first().description)

    
    def test_other_factory_users_cannot_create_property(self):
        """Test that other factory users cannot create property"""

        # create another factory
        factory2 = Factory.objects.create(
            name="Factory 2",
            address="Factory 2 address",
            city="Factory 2 city",
            country="Factory 2 country",
        )
        # create a equipment in factory2
        equipment2 = Equipment.objects.create(
            factory=factory2,
            name="Equipment 2",
            description="Equipment 2 description",
            price=100.00,
            date="2021-01-01",
            status=True,
        )
        # create a user for factory2
        user2 = get_user_model().objects.create_user(
            email="ru2@test.com",
            password="testpass",
        )
        user2.is_staff = False
        user2.factory = factory2
        user2.save()

        # logout current user
        self.client.logout()
        self.client.force_authenticate(user2)

        # try to create property in factory1
        payload = {
            "name": "Property 1",
            "description": "Property 1 description",
            "equipment": self.equipment.id,
        }
        res = self.client.post(
            reverse("equipment:create_property", args=[self.equipment.id]), payload
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_equipment_successful(self):
        """Test updating an equipment"""
        payload = {
            "name": "Equipment 2",
            "factory": self.factory.id,
            "description": "Equipment 2 description",
            "price": 200.00,
            "date": "2021-01-01",
            "status": True,
        }
        res = self.client.put(UPDATE_EQUIPMENT_URL, payload, args=[self.equipment.id])
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        equipment = Equipment.objects.get(id=res.data["id"])
        self.assertEqual(payload["name"], equipment.name)
        self.assertEqual(payload["description"], equipment.description)
        self.assertEqual(payload["price"], equipment.price)


    def test_other_factory_users_cannot_update_property(self):
        """Test that other factory users cannot update property"""

        # create another factory
        factory2 = Factory.objects.create(
            name="Factory 2",
            address="Factory 2 address",
            city="Factory 2 city",
            country="Factory 2 country",
        )
        # create a equipment in factory2
        equipment2 = Equipment.objects.create(
            factory=factory2,
            name="Equipment 2",
            description="Equipment 2 description",
            price=100.00,
            date="2021-01-01",
            status=True,
        )
        # create a user for factory2
        user2 = get_user_model().objects.create_user(
            email="ru2@test.com",
            password="testpass",
        )

        user2.is_staff = False
        user2.factory = factory2
        user2.save()

        # create a property for equipment2
        property2 = equipment2.property_set.create(
            name="Property 2",
            description="Property 2 description",
        )

        # logout current user
        self.client.logout()
        self.client.force_authenticate(user2)

        # try to update property in factory1
        payload = {
            "name": "Property 2",
            "description": "Property 2 description",
            "equipment": equipment2.id,
        }
        res = self.client.put(
            reverse("equipment:update_property", args=[property2.id]), payload
        )

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_delete_equipment_successful(self):
        """Test deleting an equipment"""
        res = self.client.delete(DELETE_EQUIPMENT_URL, args=[self.equipment.id])
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        equipment = Equipment.objects.filter(id=self.equipment.id)
        self.assertEqual(len(equipment), 0)

    def test_other_factory_users_cannot_delete_property(self):
        """Test that other factory users cannot delete property"""

        # create another factory
        factory2 = Factory.objects.create(
            name="Factory 2",
            address="Factory 2 address",
            city="Factory 2 city",
            country="Factory 2 country",
        )
        # create a equipment in factory2
        equipment2 = Equipment.objects.create(
            factory=factory2,
            name="Equipment 2",
            description="Equipment 2 description",
            price=100.00,
            date="2021-01-01",
            status=True,
        )
        # create a user for factory2
        user2 = get_user_model().objects.create_user(
            email="ru2@test.com",
            password="testpass",
        )

        user2.is_staff = False
        user2.factory = factory2
        user2.save()

        # create a property for equipment2
        property2 = equipment2.property_set.create(
            name="Property 2",
            description="Property 2 description",
        )
        
        # logout current user
        self.client.logout()
        self.client.force_authenticate(user2)
        
        # try to delete property in factory1
        res = self.client.delete(
            reverse("equipment:delete_property", args=[property2.id])
        )

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        