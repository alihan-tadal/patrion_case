from django.urls import path
from equipment.views import (
    EquipmentListByFactoryIdAPIView,
    CreateEquipmentAPIView,
    UpdateEquipmentAPIView,
    DeleteEquipmentAPIView,
    CreatePropertyAPIView,
    DeletePropertyAPIView,
    UpdatePropertyAPIView,
)


app_name = "equipment"

urlpatterns = [
    # All Users
    path("create/", CreateEquipmentAPIView.as_view(), name="create"),
    path("list/<int:pk>/", EquipmentListByFactoryIdAPIView.as_view(), name="list"),
    path("update/<int:pk>/", UpdateEquipmentAPIView.as_view(), name="update"),
    path("delete/<int:pk>/", DeleteEquipmentAPIView.as_view(), name="delete"),
    # Property API
    path(
        "create_property/<int:pk>/",
        CreatePropertyAPIView.as_view(),
        name="create_property",
    ),
    path(
        "update_property/<int:pk>/",
        UpdatePropertyAPIView.as_view(),
        name="update_property",
    ),
    path(
        "delete_property/<int:pk>/",
        DeletePropertyAPIView.as_view(),
        name="delete_property",
    ),
]
