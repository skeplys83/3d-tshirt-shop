import logging

logger = logging.getLogger(__name__)

from rest_framework import generics, status
from .permissions import IsAdminGroupUser
from rest_framework.permissions import AllowAny
from .models import Product
from rest_framework.response import Response
from .serializers import ProductSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminGroupUser()]
        return [AllowAny()]

    def get(self, request, *args, **kwargs):
        logger.info("GET request für alle Produkte")
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.is_staff:
            logger.info("POST request for new product")
            logger.debug(f"POST data: {request.data}")
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.error(f"Fehler bei der Validierung: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Not authorized to create products."}, status=status.HTTP_403_FORBIDDEN)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE', 'PATCH', 'OPTIONS']:
            return [IsAdminGroupUser()]
        return [AllowAny()]

    def get(self, request, *args, **kwargs):
        logger.info(f"GET request für Produkt ID: {kwargs['id']}")
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        # Nur Admins dürfen Produkte aktualisieren
        if request.user.is_staff:
            logger.info(f"PUT request für Produkt ID: {kwargs['id']}")
            logger.debug(f"PUT Daten: {request.data}")
            return self.update(request, *args, **kwargs)
        else:
            return Response({"detail": "Not authorized to update products."}, status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, *args, **kwargs):
        # Nur Admins dürfen Produkte aktualisieren
        if request.user.is_staff:
            logger.info(f"PATCH request für Produkt ID: {kwargs['id']}")
            logger.debug(f"PATCH Daten: {request.data}")
            return self.partial_update(request, *args, **kwargs)
        else:
            return Response({"detail": "Not authorized to update products."}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        # Nur Admins dürfen Produkte löschen
        if request.user.is_staff:
            logger.info(f"DELETE request für Produkt ID: {kwargs['id']}")
            return self.destroy(request, *args, **kwargs)
        else:
            return Response({"detail": "Not authorized to delete products."}, status=status.HTTP_403_FORBIDDEN)
