from abc import ABC, abstractmethod


class ProcesadorPago(ABC):
    """
    D - Inversión de Dependencias (DIP).
    Define el CONTRATO que cualquier procesador de pago debe cumplir.
    La capa de servicio depende de esta abstracción, no de una
    implementación concreta.
    """

    @abstractmethod
    def pagar(self, monto: float) -> bool:
        ...
