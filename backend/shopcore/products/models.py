from django.db import models


class Product(models.Model):
    SIZE_CHOICES = (
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
    )

    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stripePriceId = models.TextField(max_length=200, null=True)
    stock = models.JSONField(default=dict)  # Example: {"XS": 10, "S": 15, "M": 5}
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    productBlenderModel = models.BinaryField(blank=True, null=True)
    productPicture = models.BinaryField(blank=True, null=True)
    colors = models.JSONField(default=list)  # Example: ["Red", "Blue", "Green"]
    category = models.JSONField(default=list)
    discount = models.BooleanField(default=False)
    discountInPercent = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def get_discounted_price(self):
        """Calculate and return the discounted price if a discount is active."""
        if self.discount:
            return self.price * (1 - self.discountInPercent / 100)
        return self.price
