from django.urls import path

from .api.views import (
    CompraAPIView,
    InventarioAPIView,
    ProductosAPIView,
)
from .views import CompraRapidaView

urlpatterns = [
    # Puerta HTML (reutiliza el Service Layer)
    path('compra-rapida/<int:libro_id>/', CompraRapidaView.as_view(),
         name='compra_rapida'),

    # API v1 — atendida por el MONOLITO Django (sigue vigente tras el estrangulamiento)
    path('api/v1/comprar/', CompraAPIView.as_view(), name='api_comprar'),
    path('api/v1/inventario/', InventarioAPIView.as_view(), name='api_inventario'),
    path('api/v1/productos/', ProductosAPIView.as_view(), name='api_productos'),
]
