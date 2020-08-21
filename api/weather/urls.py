from django.conf.urls import url
from .views import CustomerListView


urlpatterns = [
    url(r'customers/', CustomerListView.as_view(), name="customers-all")
]
