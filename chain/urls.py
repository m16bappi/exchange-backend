from django.urls import path

from .views import AssetListCreateAPIView

urlpatterns = [
    path('asset/', AssetListCreateAPIView.as_view()),
]
