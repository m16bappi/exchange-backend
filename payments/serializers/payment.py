from rest_framework import serializers

# ------------ import internal modules --------------
from ..models import Payment
from chain.models import Asset
from chain.serializers import AssetSerializer


class PaymentSerializer(serializers.ModelSerializer):
    base_asset = AssetSerializer(read_only=True)
    payment_address = serializers.StringRelatedField()  # type: ignore
    network = serializers.CharField(max_length=255, write_only=True, required=True)
    symbol = serializers.CharField(max_length=255, write_only=True, required=True)
    status = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = (
            'payment_address',
            'paid_amount',
            'tx_hash',
            'status',
        )

    def validate(self, attrs: dict):
        network: str = attrs.pop('network')
        symbol: str = attrs.pop('symbol')

        asset_by_networks = Asset.objects.filter(network__name=network.upper())
        asset = asset_by_networks.filter(symbol=symbol.upper()).first()

        errors = dict()

        if not asset_by_networks:
            errors['network'] = 'Select correct network'

        if not asset:
            errors['symbol'] = 'select correct asset'

        if errors:
            raise serializers.ValidationError(errors)

        attrs['base_asset'] = asset
        return attrs

    def create(self, validated_data):
        return super(PaymentSerializer, self).create(validated_data)
