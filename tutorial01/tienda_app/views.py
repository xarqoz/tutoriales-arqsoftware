from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .infra.gateways import BancoNacionalProcesador
from .services import CompraRapidaService


class CompraRapidaView(View):
    """CBV delgada: solo es el puente entre la web y el servicio de negocio."""

    template_name = 'tienda_app/compra_rapida.html'

    def _servicio(self):
        return CompraRapidaService(procesador_pago=BancoNacionalProcesador())

    def get(self, request, libro_id):
        libro, total = self._servicio().obtener_total_estimado(libro_id)
        return render(request, self.template_name, {'libro': libro, 'total': total})

    def post(self, request, libro_id):
        try:
            total = self._servicio().procesar(libro_id)
        except ValueError as e:
            return HttpResponse(str(e), status=400)
        return HttpResponse(f"Compra exitosa. Total: ${total}")
