from django.urls import path

from .api.views import CompraAPIView, InventarioAPIView
from .views import CompraRapidaView

urlpatterns = [
    # Puerta HTML (reutiliza el Service Layer)
    path('compra-rapida/<int:libro_id>/', CompraRapidaView.as_view(),
         name='compra_rapida'),

    # Puerta API (reutiliza el MISMO Service Layer)
    path('api/v1/comprar/', CompraAPIView.as_view(), name='api_comprar'),
    path('api/v1/inventario/', InventarioAPIView.as_view(), name='api_inventario'),
]
