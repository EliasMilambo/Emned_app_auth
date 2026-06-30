from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from products.models import Product


class Invoice(models.Model):
    STATUS_CHOICES = (
        ('DRAFT', 'Brouillon'),
        ('SENT', 'Envoyée'),
        ('PAID', 'Payée'),
        ('CANCELLED', 'Annulée'),
    )

    invoice_number = models.CharField(max_length=50, unique=True, verbose_name="Numéro de facture")
    client_name = models.CharField(max_length=150, verbose_name="Nom du client")
    client_email = models.EmailField(verbose_name="Email du client")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT', verbose_name="Statut")
    tax_rate = models.DecimalField(max_digits=4, decimal_places=2, default=20.00, verbose_name="Taux de TVA (%)")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'émission")
    due_date = models.DateField(verbose_name="Date d'échéance")
    paid_at = models.DateTimeField(blank=True, null=True, verbose_name="Date de paiement")

    class Meta:
        verbose_name = "Facture"
        verbose_name_plural = "Factures"
        ordering = ['-created_at']

    def __str__(self):
        return f"Facture {self.invoice_number} - {self.client_name}"

    @property
    def total_ht(self):
        """Calcule le total Hors Taxe à partir des lignes de la facture"""
        return sum(item.total_line_ht for item in self.items.all())

    @property
    def total_tva(self):
        """Calcule le montant de la TVA"""
        return (self.total_ht * self.tax_rate) / Decimal('100.00')

    @property
    def total_ttc(self):
        """Calcule le total Toutes Taxes Comprises"""
        return self.total_ht + self.total_tva


class InvoiceItem(models.Model):
    """Ligne de détail de la facture (Lie le produit au moment de la vente)"""
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items', verbose_name="Facture")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name="Produit")
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)], verbose_name="Quantité")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2,
                                     verbose_name="Prix unitaire HT (au moment de la vente)")

    @property
    def total_line_ht(self):
        return self.quantity * self.unit_price