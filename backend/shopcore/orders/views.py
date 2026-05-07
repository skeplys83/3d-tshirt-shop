from rest_framework import generics, status
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from .permissions import IsAdminGroupUser


class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminGroupUser]

    def get(self, request, *args, **kwargs):
        """List all orders (admin only)."""
        # Nur Admins dürfen alle Bestellungen sehen, siehe Permissions
        return self.list(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     """Create a new order."""
    #    serializer = self.get_serializer(data=request.data)
    #    serializer.is_valid(raise_exception=True)

    #    if request.user.is_authenticated:
    #        serializer.save(orderPlacedByUserWithId=request.user.id)
    #    else:
    #        # If the user is not authenticated, save without a user reference
    #        serializer.save()

    #    return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminGroupUser]

    def get(self, request, *args, **kwargs):
        """Retrieve a specific order by ID."""
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Update an existing order (admin only)."""
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Delete a specific order (admin only)."""
        return self.destroy(request, *args, **kwargs)


class OrdersByUserIdView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAdminGroupUser]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Order.objects.filter(orderPlacedByUserWithId=user_id).exclude(status='cancelled').order_by('-id')


