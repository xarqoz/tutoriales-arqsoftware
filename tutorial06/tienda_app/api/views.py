from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from tienda_app.infra.factories import PaymentFactory
from tienda_app.models import Libro
from tienda_app.services import CompraService  # <--- REUTILIZACIÓN del Service Layer

from .serializers import LibroSerializer, OrdenInputSerializer


class CompraAPIView(APIView):
    """
    Endpoint para procesar compras vía JSON.

        POST /api/v1/comprar/
        Payload: {"libro_id": 1, "direccion_envio": "Calle 123", "cantidad": 1}

    La API View NO reescribe la lógica de compra: actúa como un nuevo cliente
    del mismo CompraService que usa la vista HTML.
    """

    def post(self, request):
        # 1. Validación de datos de entrada (Adapter / DTO).
        serializer = OrdenInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        datos = serializer.validated_data

        try:
            # 2. Inyección de dependencias (Factory).
            gateway = PaymentFactory.get_processor()

            # 3. Ejecución de la lógica de negocio (Service Layer).
            servicio = CompraService(procesador_pago=gateway)
            usuario = request.user if request.user.is_authenticated else None
            resultado = servicio.ejecutar_compra(
                libro_id=datos['libro_id'],
                cantidad=datos.get('cantidad', 1),
                direccion=datos['direccion_envio'],
                usuario=usuario,
            )

            return Response(
                {'estado': 'exito', 'mensaje': f'Orden creada. Total: {resultado}'},
                status=status.HTTP_201_CREATED,
            )

        except ValueError as e:
            # Errores de negocio (ej.: sin stock).
            return Response({'error': str(e)}, status=status.HTTP_409_CONFLICT)
        except Exception:
            # Errores inesperados.
            return Response(
                {'error': 'Error interno'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class InventarioAPIView(APIView):
    """
    GET /api/v1/inventario/

    Lista los libros con su stock_actual. Sirve para EVIDENCIAR que, tras una
    compra por la API, el inventario se descuenta (la misma lógica que vería
    la vista HTML de inventario).
    """

    def get(self, request):
        libros = Libro.objects.all()
        serializer = LibroSerializer(libros, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductosAPIView(APIView):
    """
    GET /api/v1/productos/

    Lista los productos (libros) servidos por el MONOLITO Django (v1). Se usa
    como prueba de COEXISTENCIA del Strangler Pattern: la ruta /api/v1/ sigue
    atendida por Django mientras /api/v2/comprar ya la atiende el microservicio
    Flask. La respuesta incluye un marcador 'servido_por' para evidenciarlo.
    """

    def get(self, request):
        libros = Libro.objects.all()
        serializer = LibroSerializer(libros, many=True)
        return Response(
            {'servido_por': 'Monolito Django (v1)', 'productos': serializer.data},
            status=status.HTTP_200_OK,
        )
