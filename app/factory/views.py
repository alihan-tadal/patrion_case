from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from core.models import Factory
from factory.serializers import FactorySerializer


# Create your views here.
class ListFactoryView(generics.ListAPIView):
    serializer_class = FactorySerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Factory.objects.all()
        else:
            return Factory.objects.filter(user=user)


class RetrieveFactoryByIdView(generics.RetrieveAPIView):
    """For admin user, retrieve factory by id. For factory user, retrieve only their factories by id."""

    serializer_class = FactorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Factory.objects.all()
    lookup_field = "pk"
    lookup_url_kwarg = "pk"


class CreateFactoryView(generics.CreateAPIView):
    """Create a new factory"""

    serializer_class = FactorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        serializer.save()


class UpdateFactoryByIdView(generics.UpdateAPIView):
    """Update factory by id"""

    serializer_class = FactorySerializer
    permission_classes = [IsAuthenticated]
    ## many to many field
    lookup_field = "pk"
    lookup_url_kwarg = "pk"

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Factory.objects.all()
        else:
            return Factory.objects.filter(user=user)

    def perform_update(self, serializer):
        serializer.save()


class DeleteFactoryByIdView(generics.DestroyAPIView):
    """Delete factory by id"""

    serializer_class = FactorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Factory.objects.all()
    lookup_field = "pk"
    lookup_url_kwarg = "pk"


