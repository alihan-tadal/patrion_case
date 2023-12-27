from django.urls import path
from factory import views


app_name = "factory"

urlpatterns = [
    # All Users
    path(
        "", views.ListFactoryView.as_view(), name="list"
    ),  # If admin user, list all factories. If factory user, list only their factories.
    path("update/<int:pk>/", views.UpdateFactoryByIdView.as_view(), name="update"),
    # Admin User
    path("create/", views.CreateFactoryView.as_view(), name="create"),
    path("<int:pk>/", views.RetrieveFactoryByIdView.as_view(), name="detail"),
    path("delete/<int:pk>/", views.DeleteFactoryByIdView.as_view(), name="delete"),
]
