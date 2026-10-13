from django.shortcuts import render
from django.views import View

from .infra.factories import PaymentFactory
from .services import CompraService


class CompraRapidaView(View):
    """CBV (puerta HTML): recibe la petición y delega al mismo CompraService."""

    template_name = 'tienda_app/compra_rapida.html'

    def _servicio(self):
        return CompraService(procesador_pago=PaymentFactory.get_processor())

    def get(self, request, libro_id):
        contexto = self._servicio().obtener_detalle_producto(libro_id)
        return render(request, self.template_name, contexto)

    def post(self, request, libro_id):
        try:
            total = self._servicio().ejecutar_compra(libro_id, cantidad=1)
        except (ValueError, Exception) as e:
            return render(request, self.template_name, {'error': str(e)}, status=400)
        return render(
            request,
            self.template_name,
            {'mensaje_exito': f"¡Gracias por su compra! Total: ${total}", 'total': total},
        )
