from rest_framework import routers
from api.weather.viewsets import CustomerViewSet

router = routers.DefaultRouter()

router.register(r'customers', CustomerViewSet)
