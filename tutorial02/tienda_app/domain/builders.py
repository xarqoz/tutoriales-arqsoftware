from decimal import Decimal

from ..models import Orden
from .logic import CalculadorImpuestos


class OrdenBuilder:
    """
    BUILDER (Paso 2).

    Ensambla una Orden paso a paso con una Fluent Interface. Encapsula la
    lógica de cálculo (subtotal + IVA) y la validación de datos mínimos,
    de modo que la Orden NUNCA se crea en un estado inconsistente.
    """

    def __init__(self):
        self.reset()

    def reset(self):
        self._usuario = None
        self._items = []
        self._direccion = ""

    def con_usuario(self, usuario):
        self._usuario = usuario
        return self  # Permite Fluent Interface

    def con_productos(self, productos):
        self._items = productos
        return self

    def para_envio(self, direccion):
        self._direccion = direccion
        return self

    def build(self) -> Orden:
        if not self._usuario or not self._items:
            raise ValueError("Datos insuficientes para crear la orden.")

        # Encapsulamos la lógica de cálculo (subtotal + IVA).
        subtotal = sum(Decimal(str(p.precio)) for p in self._items)
        total_con_iva = Decimal(str(CalculadorImpuestos.obtener_total_con_iva(subtotal)))

        orden = Orden.objects.create(
            usuario=self._usuario,
            libro=self._items[0],          # representante de la orden (modelo con FK a Libro)
            total=total_con_iva,
            direccion_envio=self._direccion,
        )
        self.reset()
        return orden
