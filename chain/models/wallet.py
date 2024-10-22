from decimal import Decimal
from django.db import models
from django.contrib import admin
from django.db.models import UniqueConstraint

from users.models import User
from .asset import Asset
from .key_pair import EncryptedKeyPair


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    key_pair = models.ForeignKey(EncryptedKeyPair, on_delete=models.CASCADE)
    current_balance = models.DecimalField(
        max_digits=20, decimal_places=8, default=Decimal('0.0')
    )
    freeze_balance = models.DecimalField(
        max_digits=20, decimal_places=8, default=Decimal('0.0')
    )

    def __str__(self):
        return self.asset.symbol

    @property
    def available_balance(self) -> Decimal:
        return self.current_balance - self.freeze_balance

    @classmethod
    def generate(cls, user: User, asset: Asset):
        key_pair = cls.get_or_create_key_pair(user, asset)
        return cls.objects.create(user=user, key_pair=key_pair, asset=asset)

    @classmethod
    def get_or_create_key_pair(cls, user: User, asset: Asset):
        existing_wallet = cls.objects.filter(
            user=user,
            asset__network__family=asset.network.family,
        ).first()

        if existing_wallet:
            return existing_wallet.key_pair

        account = asset.network.get_account()
        key_pair = EncryptedKeyPair.generate(account)

        return key_pair

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'asset'],
                name='unique_user_asset_wallet',
            )
        ]


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = [
        'asset',
        'key_pair',
        'available_balance',
        'current_balance',
        'freeze_balance',
    ]
