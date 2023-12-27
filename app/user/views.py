from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated

from user.serializers import UserSerializer


class RetrieveUserView(generics.RetrieveAPIView):
    """Retrieve authenticated user"""

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""

    ## only staff can create new user
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]


class RetrieveUserByIdView(generics.RetrieveAPIView):
    """Retrieve user by id"""

    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = get_user_model().objects.all()
    lookup_field = "pk"
    lookup_url_kwarg = "pk"


class UpdateUserByIdView(generics.UpdateAPIView):
    """Update user by id"""

    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = get_user_model().objects.all()
    lookup_field = "pk"
    lookup_url_kwarg = "pk"


class DeleteUserByIdView(generics.DestroyAPIView):
    """Delete user by id"""

    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = get_user_model().objects.all()
    lookup_field = "pk"
    lookup_url_kwarg = "pk"


class ListUserView(generics.ListAPIView):
    """List all users"""

    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    

    def get_queryset(self):
        """Return all users"""
        if get_user_model().objects.first() == self.request.user:
            return self.queryset.all()
        elif self.request.user.is_staff:
            return self.queryset.all()
        else:
            return self.queryset.filter(factory=self.request.user.factory)