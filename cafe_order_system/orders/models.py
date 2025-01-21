from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    STATUS_CHOICES = [
        ('В ожидании', 'В ожидании'),
        ('Готово', 'Готово'),
        ('Оплачено', 'Оплачено'),
    ]
    table_number = models.IntegerField(unique=True, blank=True, null=True)
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_name', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='В ожидании', blank=True, null=True)

    def __str__(self):
        return f"Status {self.status} for table {self.table_number}"

