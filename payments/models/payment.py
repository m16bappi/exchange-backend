from decimal import Decimal
from django.db import models
from django.contrib import admin
from django.http.request import HttpRequest
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

# -------------- import internal modules --------------
from chain.models import Asset, EncryptedKeyPair


class PaymentStatus(models.IntegerChoices):
    ACCEPTED = 0, _('accepted')
    PENDING = 1, _('pending')
    CONFIRMED = 2, _('confirmed')


class Payment(models.Model):
    base_asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE,
        related_name='asset'
    )
    payment_address = models.ForeignKey(
        EncryptedKeyPair,
        on_delete=models.CASCADE,
        related_name='key_pair'
    )
    received_address = models.CharField(max_length=255)
    '''
    Todo: will add validator, Asset model should have max_limit and min_limit feature amount
    should be between min and max limit bound.
    '''
    amount = models.DecimalField(
        max_digits=18,
        decimal_places=12,
        validators=[MinValueValidator(Decimal(0.01))]
    )
    paid_amount = models.DecimalField(max_digits=18, decimal_places=12)
    tx_hash = models.CharField(max_length=255)
    status = models.IntegerField(
        choices=PaymentStatus.choices,
        default=PaymentStatus.ACCEPTED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payment'
        verbose_name = 'payment'
        verbose_name_plural = 'payments'


@admin.register(Payment)
class AdminPayment(admin.ModelAdmin):
    list_display = [
        'base_asset',
        'payment_address',
        'received_address',
        'amount',
        'paid_amount',
        'tx_hash',
        'status',
    ]

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return False
