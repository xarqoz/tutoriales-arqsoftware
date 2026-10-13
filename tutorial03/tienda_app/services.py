from django.shortcuts import get_object_or_404

from .domain.builders import OrdenBuilder
from .domain.logic import CalculadorImpuestos
from .models import Inventario, Libro, Orden


class CompraService:
    """
    SERVICE LAYER reutilizable.

    Punto clave del Tutorial 03: este MISMO servicio es consumido tanto por
    la vista HTML (CompraRapidaView) como por la API REST (CompraAPIView).
    Ambas "puertas" conducen a la misma "habitación" (la lógica de negocio):
    descuenta inventario, construye la orden con el Builder y paga con el
    procesador que entrega la Factory.
    """

    def __init__(self, procesador_pago):
        self.procesador_pago = procesador_pago
        self.builder = OrdenBuilder()

    def obtener_detalle_producto(self, libro_id):
        libro = get_object_or_404(Libro, id=libro_id)
        total = CalculadorImpuestos.obtener_total_con_iva(libro.precio)
        return {"libro": libro, "total": total}

    def ejecutar_compra(self, libro_id, cantidad=1, direccion="", usuario=None):
        libro = get_object_or_404(Libro, id=libro_id)
        inv = get_object_or_404(Inventario, libro=libro)

        if inv.cantidad < cantidad:
            raise ValueError("No hay suficiente stock para completar la compra.")

        orden = (
            self.builder
            .con_usuario(usuario)
            .con_libro(libro)
            .con_cantidad(cantidad)
            .para_envio(direccion)
            .build()
        )

        if not self.procesador_pago.pagar(orden.total):
            orden.delete()
            raise Exception("La transacción fue rechazada por el banco.")

        inv.cantidad -= cantidad
        inv.save()
        return orden.total
