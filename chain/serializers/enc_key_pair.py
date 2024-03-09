from rest_framework import serializers

from ..models import EncryptedKeyPair


class EncryptedKeyPairSerializer(serializers.ModelSerializer):
    class Meta:
        model = EncryptedKeyPair
        fields = ('address',)
