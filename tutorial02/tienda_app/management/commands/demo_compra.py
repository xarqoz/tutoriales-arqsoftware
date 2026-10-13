from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from tienda_app.infra.factories import PaymentFactory
from tienda_app.models import Libro
from tienda_app.services import CompraService


class Command(BaseCommand):
    help = (
        "Demuestra Factory Method + Builder ejecutando una compra. "
        "Con PAYMENT_PROVIDER=MOCK verá el mensaje [DEBUG] Mock Payment..."
    )

    def handle(self, *args, **options):
        usuario, _ = User.objects.get_or_create(username='demo')
        productos = list(Libro.objects.all()[:2])
        if not productos:
            self.stdout.write(self.style.ERROR(
                "No hay libros. Ejecute primero: python manage.py seed_datos"))
            return

        gateway = PaymentFactory.get_processor()  # Factory decide según PAYMENT_PROVIDER
        self.stdout.write(f"Procesador seleccionado: {type(gateway).__name__}")

        servicio = CompraService(procesador_pago=gateway)
        resultado = servicio.ejecutar_proceso_compra(
            usuario=usuario,
            lista_productos=productos,
            direccion="Calle 123",
        )
        self.stdout.write(self.style.SUCCESS(resultado))
