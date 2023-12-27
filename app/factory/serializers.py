import uuid

from rest_framework import serializers
from core.models import Factory

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_field


class FactorySerializer(serializers.ModelSerializer):
   
    ## add extrafield and extract created factory's user id
    user_id = serializers.SerializerMethodField(help_text="Id of the first user in this factory")
    user_email = serializers.SerializerMethodField(help_text="Email of the first user in this factory")
    all_users = serializers.SerializerMethodField(help_text="All users in this factory")
    equipments = serializers.SerializerMethodField(help_text="All equipments in this factory")

    class Meta:
        model = Factory
        fields = ["id", "name", "address", "city", "country", "user_id", "user_email", "all_users", "equipments"]
        read_only_fields = ["id", ]

    def create(self, validated_data):
        newly_created_user = get_user_model().objects.create_user(
            email=f"{uuid.uuid4()}@factory.com",
            password="changeme",
            name=self.validated_data["name"],
            surname="Default Surname",
            is_staff=True,
        )
        instance = super().create(validated_data)
        newly_created_user.factory = instance
        newly_created_user.save()
        return instance
    
    @extend_schema_field(int)
    def get_user_id(self, obj):
        if obj.user_set.first() is None:
            return None
        return obj.first_user_id
    
    @extend_schema_field(str)
    def get_user_email(self, obj):
        if obj.user_set.first() is None:
            return None
        return obj.user_set.first().email
    
    @extend_schema_field(list)
    def get_all_users(self, obj):
        # use dict comprehension to get all users
        return [{"id": user.id, "email": user.email, "is_staff": user.is_staff} for user in obj.user_set.all()]
    
    @extend_schema_field(list)
    def get_equipments(self, obj):
        equipments = obj.equipments.all()
        return [{"id": equipment.id, "name": equipment.name, "description": equipment.description, "price": equipment.price, "date": equipment.date, "status": equipment.status} for equipment in equipments]