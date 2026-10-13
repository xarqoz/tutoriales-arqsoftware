# Tutorial 03 — Introducción a APIs con DRF (De Monolito HTML a Backend Headless)

Añade una capa de **API REST con Django Rest Framework** que **reutiliza el mismo
Service Layer** de los tutoriales anteriores. Así, la lógica de negocio sirve tanto a
vistas HTML como a clientes JSON.

## ¿Qué entrega este tutorial?

| Archivo | Rol |
| :--- | :--- |
| `tienda_app/api/serializers.py` | `OrdenInputSerializer` (DTO de entrada) y `LibroSerializer` (Adapter de salida). |
| `tienda_app/api/views.py` | `CompraAPIView` (POST) reutiliza `CompraService`; `InventarioAPIView` (GET) muestra el stock. |
| `tienda_app/urls.py` | Expone `POST /api/v1/comprar/` y `GET /api/v1/inventario/`. |
| `tienda_app/services.py` | **El mismo servicio** consumido por la vista HTML y por la API. |
| `Tienda/settings.py` | `rest_framework` agregado a `INSTALLED_APPS`. |

## Cómo ejecutar

```bash
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_datos
python manage.py runserver
```

## Cómo generar la evidencia

**1) Captura del POST a la API (Postman o la interfaz web de DRF):**

- Interfaz web de DRF: abra `http://127.0.0.1:8000/api/v1/comprar/` en el navegador,
  escriba el payload y pulse **POST**.
- Postman: `POST http://127.0.0.1:8000/api/v1/comprar/` con body JSON:

```json
{ "libro_id": 1, "direccion_envio": "Calle 123", "cantidad": 1 }
```

Respuesta esperada (201):
```json
{ "estado": "exito", "mensaje": "Orden creada. Total: ..." }
```

**2) Prueba de que ambas "puertas" llegan a la misma lógica:**

- Antes de comprar: `GET http://127.0.0.1:8000/api/v1/inventario/` → anote el `stock_actual`.
- Haga el POST a `/api/v1/comprar/`.
- Después: vuelva a `GET /api/v1/inventario/` → el `stock_actual` del libro bajó en 1.
- Además, se añadió una línea al log de pagos (`pagos_locales_SU_NOMBRE.log`), igual que
  en el Tutorial 01, porque usa la **misma** Factory/gateway.

> Esto prueba que comprar por API descuenta inventario y genera el log, exactamente como
> la compra por HTML: ambas puertas conducen a la misma "habitación" (la lógica de negocio).

## Notas de arquitectura

La `CompraAPIView` no reimplementa nada: valida la entrada (serializer), pide el procesador
a la Factory e invoca `CompraService.ejecutar_compra(...)`. El servicio es idéntico al que
usa `CompraRapidaView` (HTML).
