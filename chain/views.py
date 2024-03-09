from rest_framework.generics import ListCreateAPIView

from chain.models import Asset
from chain.serializers.asset import AssetSerializer


class AssetListCreateAPIView(ListCreateAPIView):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
