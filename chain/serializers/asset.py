from rest_framework import serializers

from chain.models import Asset


class AssetSerializer(serializers.ModelSerializer):
    network = serializers.StringRelatedField()  # type: ignore

    class Meta:
        model = Asset
        fields = (
            'symbol',
            'network',
        )
