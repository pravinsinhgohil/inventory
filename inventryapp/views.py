from django.shortcuts import render

from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from .models import Inventory
from .serializers import InventorySerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password or not email:
            return Response({"error": "Please provide all required fields"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        # Generate tokens for the user
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class InventoryListView(generics.ListAPIView):
    """
    this functionality used to get all records if authorized.
    """
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # Check if cached data exists
        cached_products = cache.get('products')

        if cached_products is None:
            # Fetch from the database if not cached
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)

            # Cache the result for 5 minutes
            cache.set('products', serializer.data, timeout=60 * 5)
        else:
            # Use cached data
            serializer = cached_products

        return Response(serializer.data, status=status.HTTP_200_OK)


class InventoryRetrieveView(generics.RetrieveAPIView):

    """
    Authorized user get single record based on key.
    """
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        cached_product = cache.get(f'product_{pk}')
        if cached_product:
            # If cached, return the cached data
            return Response(cached_product, status=status.HTTP_200_OK)

        try:
            # If not cached, retrieve product from the database
            product = Inventory.objects.get(pk=pk)
        except Inventory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Serialize the product data
        serializer = InventorySerializer(product)

        # Cache the product data for 5 minutes
        cache.set(f'product_{pk}', serializer.data, timeout=60 * 5)

        return Response(serializer.data, status=status.HTTP_200_OK)


class InventoryCreateView(generics.CreateAPIView):

    """
    Authorized user can add new inventory record.
    """
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            serializer.save()  # Save the new product instance
            # Invalidate the cache when a new product is created
            cache.delete('products')
        except Exception as e:
            # If there's an error, you might want to log it or handle it further
            # Here we can return a 500 status code for a server error
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class InventoryUpdateView(generics.UpdateAPIView):
    """
    Authorized user can update the inventory record.
    """
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    lookup_field = 'pk'  # Specify the field used for lookup (default is 'pk')

    def perform_update(self, serializer):
        """
        UPDATE the record using primary key
        """
        try:
            serializer.save()  # Save the updated product instance
            # Invalidate the cache when a product is updated
            cache.delete(f'product_{self.kwargs["pk"]}')
            cache.delete('products')
        except Exception as e:
            # If there's an error, return a 500 status code for server error
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class InventoryDestroyView(generics.DestroyAPIView):
    """
    Authorized user delete the record based on the key.

    """
    queryset = Inventory.objects.all()  # Base queryset for the view
    serializer_class = InventorySerializer  # Serializer to validate input data
    lookup_field = 'pk'  # Specify the field used for lookup (default is 'pk')
    permission_classes = [IsAuthenticated]  # Ensure that only authenticated users can delete inventory items

    def perform_destroy(self, instance):
        try:
            # Invalidate the cache before deletion
            cache.delete(f'product_{instance.pk}')
            cache.delete('products')
            instance.delete()  # Delete the inventory item
        except Exception as e:
            raise Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

