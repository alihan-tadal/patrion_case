from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from user import views

app_name = "user"

urlpatterns = [
    ## All Users
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", views.RetrieveUserView.as_view(), name="me"),
    ## Admin User
    path("create/", views.CreateUserView.as_view(), name="create"),
    path("detail/<int:pk>/", views.RetrieveUserByIdView.as_view(), name="detail"),
    path("update/<int:pk>/", views.UpdateUserByIdView.as_view(), name="update"),
    path("delete/<int:pk>/", views.DeleteUserByIdView.as_view(), name="delete"),
    path("list/", views.ListUserView.as_view(), name="list"),
]
