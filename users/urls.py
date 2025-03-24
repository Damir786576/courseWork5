from django.urls import path
from .views import UserRegistrationView, UserListView, UserDetailView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('list/', UserListView.as_view(), name='user-list'),
    path('me/', UserDetailView.as_view(), name='user-detail'),
]
