from .domain.logic import CalculadorImpuestos
from .models import Inventario, Libro, Orden


class CompraRapidaService:
    """
    SERVICE LAYER (Paso 3).

    Orquesta la lógica de negocio de la "Compra Rápida" que antes vivía
    desordenada dentro de la vista (FBV Spaghetti). Ahora:

      - El cálculo de impuestos se delega al dominio (CalculadorImpuestos).
      - El proceso de pago se delega a una abstracción inyectada
        (procesador_pago), cumpliendo DIP: el servicio NO sabe qué banco
        concreto se usa.
      - La vista solo actúa como puente web -> servicio.
    """

    def __init__(self, procesador_pago):
        self.procesador_pago = procesador_pago

    def procesar(self, libro_id):
        libro = Libro.objects.get(id=libro_id)
        inv = Inventario.objects.get(libro=libro)

        if inv.cantidad <= 0:
            raise ValueError("No hay existencias.")

        total = CalculadorImpuestos.obtener_total_con_iva(libro.precio)

        if self.procesador_pago.pagar(total):
            inv.cantidad -= 1
            inv.save()
            Orden.objects.create(libro=libro, total=total)
            return total
        return None

    def obtener_total_estimado(self, libro_id):
        """Usado por el GET para mostrar el precio con IVA sin comprar."""
        libro = Libro.objects.get(id=libro_id)
        return libro, CalculadorImpuestos.obtener_total_con_iva(libro.precio)
