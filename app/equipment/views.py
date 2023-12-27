import rest_framework.generics
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, BasePermission
from core.models import Equipment, Factory, Property
from equipment.serializers import EquipmentSerializer, PropertySerializer


class IsFactoryMember(BasePermission):
    """Check if user is a member of the factory"""

    def has_permission(self, request, view):
        """Check if user is a member of the factory"""
        if request.user.is_staff:
            return True
        factory = get_object_or_404(Factory, pk=view.kwargs.get("pk"))
        return factory.user_set.filter(id=request.user.id).exists()
        

class EquipmentListByFactoryIdAPIView(generics.ListAPIView):
    """List all equipment in given factory"""

    serializer_class = EquipmentSerializer
    permission_classes = [IsAuthenticated, IsFactoryMember]
  
    def get_queryset(self):
        """Return all equipment in given factory"""
        factory = get_object_or_404(Factory, pk=self.kwargs.get("pk"))
        return factory.equipments.all()


class CreateEquipmentAPIView(generics.CreateAPIView):
    """Create a new equipment in the system"""

    ## only staff can create new equipment
    serializer_class = EquipmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Create a new equipment"""
        factory = get_object_or_404(Factory, pk=self.kwargs.get("pk"))
        serializer.save(factory=factory)


class UpdateEquipmentAPIView(generics.UpdateAPIView):
    """Update equipment by id"""

    serializer_class = EquipmentSerializer
    permission_classes = [IsAuthenticated, IsFactoryMember]
    queryset = Equipment.objects.all()
    lookup_field = "pk"
    lookup_url_kwarg = "pk"


class DeleteEquipmentAPIView(generics.DestroyAPIView):
    """Delete equipment by id"""

    serializer_class = EquipmentSerializer
    permission_classes = [IsAuthenticated, IsFactoryMember]
    queryset = Equipment.objects.all()
    lookup_field = "pk"
    lookup_url_kwarg = "pk"


class CreatePropertyAPIView(generics.CreateAPIView):
    """Create a new property in the system"""

    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated, IsFactoryMember]

    def perform_create(self, serializer):
        """Create a new property"""
        equipment = get_object_or_404(Equipment, pk=self.kwargs.get("pk"))
        serializer.save(equipment=equipment)


class UpdatePropertyAPIView(generics.UpdateAPIView):
    """Update property by id"""

    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated, IsFactoryMember]
    queryset = Property.objects.all()
    lookup_field = "pk"
    lookup_url_kwarg = "pk"


class DeletePropertyAPIView(generics.DestroyAPIView):
    """Delete property by id"""

    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated, IsFactoryMember]
    queryset = Property.objects.all()
    lookup_field = "pk"
    lookup_url_kwarg = "pk"