from django.urls import path, include
from rest_framework import routers, urlpatterns

from rest_framework.routers import DefaultRouter

from .views import LeadViewSet, delete_lead

router = DefaultRouter()
router.register('leads', LeadViewSet, basename='leads')

urlpatterns = [
    path('leads/delete/<int:lead_id>/', delete_lead, name='delete-lead'),
    path('', include(router.urls)),
]
