from django.db import models
from customers.models import Customer

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=(
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('ready', 'Ready'),
        ('under_processing', 'Under Processing'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ), default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_name} for {self.customer.name}"

    @property
    def total_price(self):
        return self.quantity * self.unit_price
