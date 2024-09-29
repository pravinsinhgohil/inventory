from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from inventory.inventryapp.views import RegisterView, InventoryListView, InventoryRetrieveView, InventoryCreateView, \
    InventoryUpdateView, InventoryDestroyView

urlpatterns = [
    # to get all records.
    path('list', InventoryListView.as_view(), name='list_inventory'),
    # to get single record based on id
    path('retrieve/<int:pk>', InventoryRetrieveView.as_view(), name='retrieve'),
    # to add new inventory record
    path('create', InventoryCreateView.as_view(), name='create'),
    # to update record
    path('update/<int:pk>', InventoryUpdateView.as_view(), name='update'),
    # to delete inventory record
    path('delete/<int:pk>', InventoryDestroyView.as_view(), name='delete'),
    # Registration endpoint
    path('api/register/', RegisterView.as_view(), name='register'),
    # Login endpoint (token obtain pair)
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Refresh token endpoint
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]