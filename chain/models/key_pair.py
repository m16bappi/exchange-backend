from uuid import uuid4
from django.db import models
from django.contrib import admin

#  -------------- import form local modules --------------------
from chain.accounts import LocalAccount, RsaEncryptor


class EncryptedKeyPair(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    address = models.CharField(editable=False, max_length=255)
    salt = models.BinaryField(editable=False)
    payload = models.BinaryField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'key_pair'
        verbose_name = 'key_pair'
        verbose_name_plural = 'key_pairs'

    @classmethod
    def generate(cls, localAccount: LocalAccount):
        return cls.objects.create(
            address=localAccount.address,
            salt=localAccount.salt,
            payload=localAccount.payload,
        )

    def decrypt(self):
        return RsaEncryptor.decrypt(self.salt, self.payload)

    def __str__(self):
        return self.address


@admin.register(EncryptedKeyPair)
class EncryptedKeyPairModelAdmin(admin.ModelAdmin):
    list_display = ["id", "address", "created_at"]

    def has_add_permission(self, request) -> bool:
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
