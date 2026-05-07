from django.db import models


class Order(models.Model):
    STATUS_CHOICES = (
        ('new', 'New order'),
        ('in_progress', 'In progress'),
        ('in_shipment', 'In Shipment'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    alternative_address = models.JSONField(default=dict, null=True, blank=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    differentShippingAddress = models.BooleanField(default=False)
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=20)
    payedStatus = models.BooleanField(default=False)
    payed_at = models.DateTimeField(auto_now=True)
    paymentMethod = models.CharField(max_length=100, blank=True)
    salutation = models.CharField(max_length=10)  # Mr., Ms., Mx., etc.
    selectedProducts = models.JSONField(default=dict)
    street_and_number = models.CharField(max_length=255)
    termsAccepted = models.BooleanField(default=False)
    totalPrice = models.DecimalField(max_digits=20, decimal_places=2)
    orderPlacedByUserWithId = models.CharField(max_length=255, blank=True)
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
