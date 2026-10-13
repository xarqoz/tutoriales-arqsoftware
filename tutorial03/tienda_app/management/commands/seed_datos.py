from django.core.management.base import BaseCommand

from tienda_app.models import Inventario, Libro


class Command(BaseCommand):
    help = "Crea libros de prueba con stock (datos del Paso 0 del tutorial)."

    def handle(self, *args, **options):
        datos = [
            ("Clean Code en Python", 150.0, 10),
            ("Patrones de Diseño", 200.0, 10),
            ("Arquitectura Limpia", 250.0, 10),
        ]
        for titulo, precio, cantidad in datos:
            libro, creado = Libro.objects.get_or_create(
                titulo=titulo, defaults={'precio': precio}
            )
            Inventario.objects.get_or_create(
                libro=libro, defaults={'cantidad': cantidad}
            )
            estado = "creado" if creado else "ya existía"
            self.stdout.write(self.style.SUCCESS(f"[{estado}] {titulo} (id={libro.id})"))

        self.stdout.write(self.style.SUCCESS("Datos de prueba listos."))
