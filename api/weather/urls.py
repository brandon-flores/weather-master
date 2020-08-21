from django.conf.urls import url
from .views import CustomerListView, CSVLoadView


urlpatterns = [
    # url(r'customers/', CustomerListView.as_view(), name="customers-all")
    url(
        r'customers/create/$', CSVLoadView.as_view(),
        name='customer-csv-load'),
]
