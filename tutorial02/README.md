# Tutorial 02 — Patrones Creacionales en Django (Factory Method + Builder)

Optimiza la creación de objetos: **Factory Method** desacopla la infraestructura de pago
mediante variables de entorno, y **Builder** gestiona la construcción de la `Orden`.

## ¿Qué entrega este tutorial?

| Archivo | Patrón | Rol |
| :--- | :--- | :--- |
| `tienda_app/infra/factories.py` | **Factory Method** | `PaymentFactory` decide el procesador según `PAYMENT_PROVIDER`. Incluye `MockPaymentProcessor`. |
| `tienda_app/domain/builders.py` | **Builder** | `OrdenBuilder` ensambla la `Orden` con Fluent Interface + validación. |
| `tienda_app/services.py` | — | `CompraService` usa Builder + Factory inyectado. |
| `tienda_app/views.py` | — | La vista delega la elección del procesador a la Fábrica. |

## Cómo ejecutar

```bash
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_datos
```

## Cómo generar la evidencia (captura `[DEBUG] Mock Payment...`)

El entregable pide una captura de la consola mostrando el mensaje del Mock al comprar
**con la variable de entorno activada**:

```bash
# Linux / Mac / GitBash
PAYMENT_PROVIDER=MOCK python manage.py demo_compra

# Windows (PowerShell)
$env:PAYMENT_PROVIDER="MOCK"; python manage.py demo_compra
```

Salida esperada en consola (lo que debe capturar):

```
Procesador seleccionado: MockPaymentProcessor
[DEBUG] Mock Payment: Procesando pago de $... sin cargo real.
Orden 1 procesada exitosamente.
```

Sin la variable (modo producción / banco real):

```bash
python manage.py demo_compra      # usa BancoNacionalProcesador (escribe en el .log)
```

## Reflexión (entregable)

> **¿Por qué el `OrdenBuilder` reduce el riesgo de errores frente a crear la orden
> directamente en la vista?**
>
> Crear la `Orden` directamente en la vista obliga a repetir —en cada punto del código
> que necesite una orden— el cálculo del subtotal, la aplicación del IVA y las
> validaciones de datos mínimos. Esa duplicación es terreno fértil para errores:
> basta con que un desarrollador olvide aplicar el IVA, invierta un parámetro o cree
> una orden sin usuario para dejar el sistema en un estado inconsistente. El
> `OrdenBuilder` centraliza esa lógica en un único lugar: expone una interfaz fluida y
> legible (`con_usuario().con_productos().para_envio().build()`) y, sobre todo, impide
> construir una orden inválida porque `build()` valida las precondiciones y encapsula el
> cálculo. Así, la vista pasa de "saber cómo se arma una orden" a simplemente "pedir una
> orden", reduciendo la superficie de error y haciendo el código más mantenible y
> testeable.
