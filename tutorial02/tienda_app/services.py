from .domain.builders import OrdenBuilder
from .domain.logic import CalculadorImpuestos
from .models import Inventario, Libro, Orden


class CompraService:
    """
    SERVICE LAYER integrado con los patrones creacionales (Paso 3).

    - Builder: ensambla la Orden con semántica clara y validación interna.
    - Factory (inyectado): permite cambiar el comportamiento de pago sin
      cambiar el código del servicio (DIP + Factory Method).
    """

    def __init__(self, procesador_pago):
        self.procesador = procesador_pago
        self.builder = OrdenBuilder()

    def ejecutar_proceso_compra(self, usuario, lista_productos, direccion):
        # Uso del Builder: semántica clara y validación interna.
        orden = (
            self.builder
            .con_usuario(usuario)
            .con_productos(lista_productos)
            .para_envio(direccion)
            .build()
        )

        # Uso del Factory (inyectado): cambio de comportamiento sin cambio de código.
        if self.procesador.pagar(orden.total):
            return f"Orden {orden.id} procesada exitosamente."

        orden.delete()
        raise Exception("Error en la pasarela de pagos.")


class CompraRapidaService:
    """Servicio de compra rápida del Tutorial 01 (se mantiene para la vista HTML)."""

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
        libro = Libro.objects.get(id=libro_id)
        return libro, CalculadorImpuestos.obtener_total_con_iva(libro.precio)
