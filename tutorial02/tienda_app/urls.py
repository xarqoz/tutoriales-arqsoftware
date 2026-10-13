from django.urls import path

from .views import CompraRapidaView

urlpatterns = [
    path('compra-rapida/<int:libro_id>/', CompraRapidaView.as_view(),
         name='compra_rapida'),
]
