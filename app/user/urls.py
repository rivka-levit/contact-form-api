"""
URL mappings for user APIs.
"""

from django.urls import path

from user.views import CreateUserView, AuthTokenView, UserProfileView

app_name = 'user'

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('token/', AuthTokenView.as_view(), name='token'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]
