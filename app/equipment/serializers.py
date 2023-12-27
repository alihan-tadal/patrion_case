from rest_framework import serializers

from core.models import Factory, Equipment, Property

"""

class Equipment(models.Model):

    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)
    price = models.FloatField()
    date = models.DateField()
    status = models.BooleanField(default=True)
    property = models.ManyToManyField(Property, blank=True)
    

    def __str__(self):
        return self.name
"""


class EquipmentSerializer(serializers.ModelSerializer):
    """Serializer for equipment objects"""

    class Meta:
        model = Equipment
        fields = ("id", "name", "description", "price", "date", "status")
        read_only_fields = ("id",)

    def create(self, validated_data):
        """Create a new equipment"""
        return Equipment.objects.create(**validated_data)
    


class PropertySerializer(serializers.ModelSerializer):
    """Serializer for property objects"""


    class Meta:
        model = Property
        fields = ("id", "name", "description", "equipment")
        read_only_fields = ("id",)

    def create(self, validated_data):
        """Create a new property"""
        return Property.objects.create(**validated_data)