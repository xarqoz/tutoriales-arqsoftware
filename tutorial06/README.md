# Tutorial 06 — El Primer Estrangulamiento (Strangler Pattern: Django → Flask v2)

Extraemos una funcionalidad del monolito (Django) hacia un **microservicio Flask**. Nginx
decide, según la ruta, a qué backend enviar cada petición. El usuario no nota que al
comprar "sale" de un sistema y "entra" a otro.

## ¿Qué cambia respecto al Tutorial 05?

| Archivo | Cambio |
| :--- | :--- |
| `microservicio_pagos/app.py` | **Nuevo.** Microservicio Flask con `POST /api/v2/comprar`. |
| `microservicio_pagos/Dockerfile` | **Nuevo.** Imagen del microservicio (Flask + Gunicorn). |
| `docker-compose.yml` | Renombra `web`→`web_django`, añade `pagos_flask`; `nginx` depende de ambos. |
| `nginx/nginx.conf` | **Ruteo del estrangulamiento:** `/api/v1/` → Django, `/api/v2/comprar` → Flask. |
| `tienda_app/api/views.py` + `urls.py` | Añade `GET /api/v1/productos/` para la prueba de coexistencia. |

### ¿Cómo enruta Nginx?
- `http://<IP>/api/v1/...` → **Django (v1)** — monolito intacto.
- `http://<IP>/api/v2/comprar` → **Flask (v2)** — función estrangulada.

> **Nombres:** el servicio Django se llama `web_django`; Gunicorn arranca
> `Tienda.wsgi:application` (nuestro proyecto es `Tienda`, no `tienda_project`).

---

## Prueba local

```bash
docker compose up -d --build
docker compose exec web_django python manage.py migrate
docker compose exec web_django python manage.py seed_datos
docker compose ps                  # db, web_django, pagos_flask, nginx

# v1 (Django):
curl http://localhost/api/v1/productos/
# v2 (Flask):
curl -X POST http://localhost/api/v2/comprar \
     -H "Content-Type: application/json" \
     -d '{"producto_id": 1, "cantidad": 2}'
```

---

## Despliegue en AWS EC2

```bash
cd tutoriales-arqsoftware/tutorial06
git pull            # si ya tenía el repo clonado
docker compose up -d --build
docker compose exec web_django python manage.py migrate
docker compose exec web_django python manage.py seed_datos
docker ps
```
(El puerto 80 ya debe estar abierto en el Security Group desde el Tutorial 05.)

---

## Evidencias a entregar (PDF)

1. **Coexistencia (v1):** captura de Postman con `GET http://<IP-AWS>/api/v1/productos/`.
   **Responde Django** (verá `"servido_por": "Monolito Django (v1)"`). ✅
2. **Estrangulamiento (v2):** captura de Postman con `POST http://<IP-AWS>/api/v2/comprar`
   y body `{"producto_id": 1, "cantidad": 2}`. El JSON debe decir
   **"procesada exitosamente por el Microservicio Flask"**. 🔀
3. **Logs de orquestación:** salida de `docker compose logs nginx` donde se vea el
   redireccionamiento a los **dos backends distintos**. El `nginx.conf` usa un
   `log_format` personalizado que imprime `upstream=<ip>:<puerto>`:
   - `upstream=...:8000` → **Django (v1)**
   - `upstream=...:5000` → **Flask (v2)**

   Genere tráfico a ambas rutas antes de capturar:
   ```bash
   curl http://localhost/api/v1/productos/
   curl -X POST http://localhost/api/v2/comprar \
        -H "Content-Type: application/json" -d '{"producto_id": 1, "cantidad": 2}'
   docker compose logs nginx
   ```
   Verá dos líneas como:
   ```
   nginx-1 | 172.x.x.x "GET /api/v1/productos/ HTTP/1.1" status=200 -> upstream=172.x.x.x:8000 [...]
   nginx-1 | 172.x.x.x "POST /api/v2/comprar HTTP/1.1" status=200 -> upstream=172.x.x.x:5000 [...]
   ```
   Dos upstreams distintos (`:8000` Django, `:5000` Flask) = Strangler Pattern funcionando. 🧾

> 💡 Al terminar: `docker compose down` y detenga la instancia para ahorrar créditos.
