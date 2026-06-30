from django.db import models
from products.models import Product

class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='inventory', verbose_name="Produit")
    quantity = models.IntegerField(default=0, verbose_name="Stock actuel")
    min_stock_level = models.IntegerField(default=5, verbose_name="Seuil d'alerte mini")

    class Meta:
        verbose_name = "État du Stock"
        verbose_name_plural = "États des Stocks"

    def __str__(self):
        return f"Stock de {self.product.name} : {self.quantity}"

    @property
    def is_low_stock(self):
        """Déclenche une alerte visuelle parfaite pour un badge Bootstrap via HTMX"""
        return self.quantity <= self.min_stock_level