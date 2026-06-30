from django.core.validators import MinValueValidator
from django.db import models

from inventory.models import Inventory
from products.models import Product

class StockMovement(models.Model):
    MOVEMENT_TYPES = (
        ('IN', 'Entrée (Achat/Réassort)'),
        ('OUT', 'Sortie (Vente)'),
        ('CORRECTION', 'Correction (Inventaire/Perte)'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_movements', verbose_name="Produit")
    movement_type = models.CharField(max_length=15, choices=MOVEMENT_TYPES, verbose_name="Type de mouvement")
    quantity = models.IntegerField(validators=[MinValueValidator(1)], verbose_name="Quantité")
    reason = models.CharField(max_length=255, blank=True, verbose_name="Motif / Commentaire")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date du mouvement")

    class Meta:
        verbose_name = "Mouvement de Stock"
        verbose_name_plural = "Mouvements de Stock"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        """
        Logique métier critique : Met à jour automatiquement l'inventaire global
        lorsqu'un mouvement est enregistré. Idéal pour prouver votre niveau en Django.
        """
        # Récupère ou crée l'inventaire lié au produit
        inventory, created = Inventory.objects.get_or_create(product=self.product)

        if self.movement_type == 'IN':
            inventory.quantity += self.quantity
        elif self.movement_type in ['OUT', 'CORRECTION']:
            # Note : En production, vous devriez lever une exception si le stock devient négatif (hors politique commerciale)
            inventory.quantity -= self.quantity

        inventory.save()
        super().save(*args, **kwargs)
