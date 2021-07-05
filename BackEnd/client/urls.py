from django.urls import path, include
from rest_framework import routers, urlpatterns

from rest_framework.routers import DefaultRouter

from .views import ClientViewSet, NoteViewSet, convert_lead_to_client, delete_client

router = DefaultRouter()
router.register('clients', ClientViewSet, basename='clients')
router.register('notes', NoteViewSet, basename='notes')

urlpatterns = [
    path('convert-lead-to-client/', convert_lead_to_client, name='leadToClient'),
    path('client/delete/<int:client_id>/', delete_client, name='delete-client'),
    path('', include(router.urls)),
]
