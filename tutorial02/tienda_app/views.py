from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .infra.factories import PaymentFactory
from .services import CompraRapidaService


class CompraRapidaView(View):
    """
    CBV "agnóstica": no sabe qué banco se usa. Delega la decisión a la
    Fábrica (Factory Method). Antes hacía:  BancoNacionalProcesador()
    Ahora hace:                             PaymentFactory.get_processor()
    """

    template_name = 'tienda_app/compra_rapida.html'

    def _servicio(self):
        gateway = PaymentFactory.get_processor()      # Delegación total a la Fábrica
        return CompraRapidaService(procesador_pago=gateway)

    def get(self, request, libro_id):
        libro, total = self._servicio().obtener_total_estimado(libro_id)
        return render(request, self.template_name, {'libro': libro, 'total': total})

    def post(self, request, libro_id):
        try:
            total = self._servicio().procesar(libro_id)
        except ValueError as e:
            return HttpResponse(str(e), status=400)
        return HttpResponse(f"Compra exitosa. Total: ${total}")
