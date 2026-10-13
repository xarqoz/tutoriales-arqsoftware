# Tutorial 01 — Evolución de Arquitectura en Django (De Spaghetti a Grado Empresarial)

Transforma la funcionalidad **"Compra Rápida"** desde una FBV desordenada hasta una
arquitectura desacoplada con **CBV + SOLID + Service Layer**.

## ¿Qué entrega este tutorial?

Según el PDF, el entregable de código es:

| Archivo | Rol |
| :--- | :--- |
| `tienda_app/services.py` | **Service Layer**: `CompraRapidaService` orquesta toda la lógica de negocio. |
| `tienda_app/views.py` | **CBV delgada** (< 10 líneas por método): solo es el puente web → servicio. |
| `tienda_app/domain/logic.py` | `CalculadorImpuestos` (SRP/OCP): el IVA deja de estar *hardcoded* en la vista. |
| `tienda_app/domain/interfaces.py` | `ProcesadorPago` (DIP): contrato de pago. |
| `tienda_app/infra/gateways.py` | `BancoNacionalProcesador`: genera el **log de auditoría** `.log`. |

> El log que genera `gateways.py` es la **evidencia principal** del tutorial.

## Antes de ejecutar: edite su nombre en el log

Abra `tienda_app/infra/gateways.py` y reemplace `SU_NOMBRE` por su nombre y apellido:

```python
archivo_log = "pagos_locales_JUAN_PEREZ.log"   # <- su nombre real
```

## Cómo ejecutar

```bash
# 1. Entorno e instalación
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Base de datos + datos de prueba (3 libros con stock)
python manage.py migrate            # ya incluye la migración de tienda_app
python manage.py seed_datos

# (Si alguna vez cambia los modelos, regenere con: python manage.py makemigrations)

# 3. Levantar el servidor
python manage.py runserver
```

## Cómo generar la evidencia (log con ≥ 3 transacciones)

Realice **al menos 3 compras** de distintos libros. Puede hacerlo por el navegador o,
más rápido, por el shell:

```bash
python manage.py shell
```
```python
from tienda_app.services import CompraRapidaService
from tienda_app.infra.gateways import BancoNacionalProcesador
from tienda_app.models import Libro

svc = CompraRapidaService(procesador_pago=BancoNacionalProcesador())
for libro in Libro.objects.all():          # compra uno de cada libro
    svc.procesar(libro.id)
```

O por navegador: visite `http://127.0.0.1:8000/compra-rapida/<id>/` y pulse **Comprar Ya**
para los ids 1, 2 y 3.

Al terminar, en la raíz del proyecto aparecerá `pagos_locales_SU_NOMBRE.log` con ≥ 3 líneas.

## Resultado esperado

- La vista (`views.py`) tiene métodos de muy pocas líneas: delega todo al servicio.
- El archivo `pagos_locales_SU_NOMBRE.log` contiene ≥ 3 registros de transacciones.
