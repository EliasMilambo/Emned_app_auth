from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom de la catégorie")
    description = models.TextField(blank=True, verbose_name="Description")
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="Image de couverture")

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Catégorie"
    )
    name = models.CharField(max_length=200, verbose_name="Nom du produit")
    description = models.TextField(verbose_name="Description")

    # Pricing (Utilisation de DecimalField pour éviter les erreurs d'arrondi)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix")
    promo_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                      verbose_name="Prix promotionnel")

    # Inventory & Status
    stock = models.IntegerField(default=0, verbose_name="Quantité en stock")
    is_active = models.BooleanField(default=True, verbose_name="En ligne / Visible")

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def is_in_stock(self):
        return self.stock > 0

    @property
    def current_price(self):
        if self.promo_price and self.promo_price < self.price:
            return self.promo_price
        return self.price
