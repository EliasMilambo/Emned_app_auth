from django.db import models

class Customer(models.Model):
    STATUS = {
        ('paid', 'Paid'),
        ('payment pending', 'Payment Pending'),
        ('payment cancelled', 'Payment Cancelled'),
    }
    first_name = models.CharField(max_length=100)
    last_name =  models.CharField(max_length=100)
    email =  models.EmailField(max_length=254, unique=True, verbose_name="Email")
    telephone =  models.CharField(blank=True, max_length=15, unique=True, null=True, verbose_name="Telephone")
    status = models.CharField(choices=STATUS, max_length=20)
    created_at =  models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")


    class Meta:
        ordering = ['-created_at']
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return f"{self.first_name} - {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} - ({self.last_name})"