from django.urls import path
from .views import ListUsersView, UserCreateView


urlpatterns = [
    path('users/', ListUsersView.as_view(), name="users-all"),
    path('users/create/', UserCreateView.as_view(), name="user-create")
]