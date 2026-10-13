# Tutorial 05 — El Escudo Arquitectónico (Nginx + Gunicorn)

Abandonamos `runserver` y montamos una arquitectura de producción de **tres capas**:
**Nginx** (Proxy Inverso) + **Gunicorn** (servidor WSGI) + **Django**. Esta es la base para
el *Strangler Pattern* del Tutorial 06.

## ¿Qué cambia respecto al Tutorial 04?

| Archivo | Cambio |
| :--- | :--- |
| `requirements.txt` | Añade **`gunicorn`**. |
| `nginx/nginx.conf` | **Nuevo.** Proxy inverso: todo el tráfico del puerto 80 va al backend `web:8000`. |
| `docker-compose.yml` | `web` ya **no expone puertos** y arranca con **Gunicorn**; se añade el servicio **`nginx`** en el puerto 80. |

Resultado: Django queda **aislado** (solo accesible por la red interna de Docker). El único
servicio expuesto a internet es Nginx, en el puerto **80**.

> **Nombres:** el PDF usa `tienda_project.wsgi`; aquí el proyecto es **`Tienda`**, por eso el
> comando es `gunicorn Tienda.wsgi:application`.

---

## Prueba local

```bash
docker compose up -d --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py seed_datos
docker compose ps                 # deben verse db, web y nginx

# Acceso correcto (por Nginx, SIN puerto 8000):
#   http://localhost/api/v1/comprar/
```

---

## Despliegue en AWS EC2

Partiendo de una instancia con Docker ya instalado (Tutorial 04):

```bash
cd tutoriales-arqsoftware/tutorial05
docker compose up -d --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py seed_datos
docker ps                          # verifique db, web y nginx en estado "Up"
```

### Abrir el puerto 80 (Security Group)
EC2 → Security Groups → su grupo → **Edit inbound rules → Add rule**:
- **Type:** HTTP · **Port range:** `80` · **Source:** `0.0.0.0/0` → **Save rules**.

---

## Evidencias a entregar

1. **Enrutamiento (navegador):** captura de `http://<IP-EC2>/api/v1/comprar/`
   — **sin** el puerto `:8000`. Si responde, Nginx está enrutando por el puerto 80. ✅
2. **Aislamiento (terminal local):** intente `http://<IP-EC2>:8000` → debe **fallar
   (timeout)**. Captura. Demuestra que Django está protegido tras el proxy. 🔒
3. **Orquestación (terminal AWS):** captura de `docker ps` mostrando los **tres**
   contenedores `nginx`, `web` y `db` en estado **Up**. 🧩

> 💡 Al terminar: `docker compose down` y detenga la instancia para ahorrar créditos.
