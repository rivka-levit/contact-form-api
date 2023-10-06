"""
URL configuration for message APIs.
"""

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from message.views import MessageViewSet

router = DefaultRouter()
router.register('messages', MessageViewSet.as_view(), basename='message')

urlpatterns = [
    path('', include(router.urls))
]
