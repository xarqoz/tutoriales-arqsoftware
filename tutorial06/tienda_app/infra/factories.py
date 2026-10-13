import os

from .gateways import BancoNacionalProcesador


class MockPaymentProcessor:
    """
    Implementación ligera para pruebas (Mocking).
    No cobra realmente; solo imprime en consola. Útil para desarrollo/test.
    """

    def pagar(self, monto: float) -> bool:
        print(f"[DEBUG] Mock Payment: Procesando pago de ${monto} sin cargo real.")
        return True


class PaymentFactory:
    """
    FACTORY METHOD (Paso 1).

    Centraliza la decisión de QUÉ procesador de pago usar. La configuración
    viene del AMBIENTE (variable de entorno PAYMENT_PROVIDER), no del código.
    Esto hace la aplicación "Docker-Ready": podemos cambiar de banco real a
    mock sin tocar una sola línea de la vista ni del servicio.
    """

    @staticmethod
    def get_processor():
        provider = os.getenv('PAYMENT_PROVIDER', 'BANCO')

        if provider == 'MOCK':
            return MockPaymentProcessor()

        # Por defecto usamos la infraestructura real.
        return BancoNacionalProcesador()
