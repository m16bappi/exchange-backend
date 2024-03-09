from rest_framework.generics import ListCreateAPIView

# -------------- internal modules ------------------
from chain.accounts import EvmAccount
from chain.models import EncryptedKeyPair

# ------------------ self modules -------------------
from .models import Payment
from .serializers import PaymentSerializer


class PaymentListCreateAPIView(ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        account = EvmAccount.generate()
        key_pair = EncryptedKeyPair.generate(account)
        serializer.save(payment_address=key_pair)
