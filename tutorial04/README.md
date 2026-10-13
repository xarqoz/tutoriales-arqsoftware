# Tutorial 04 — Dockerización y Despliegue en AWS (De Localhost a la Nube)

Empaqueta la "Tienda API" (Tutorial 03) en contenedores **Docker** y la despliega en una
instancia **AWS EC2**. La configuración deja de "quemar" credenciales: todo pasa por
**variables de entorno** (infraestructura inmutable).

## ¿Qué entrega / cambia este tutorial?

| Archivo | Cambio |
| :--- | :--- |
| `Tienda/settings.py` | Base de datos **PostgreSQL** leída desde variables de entorno (`DB_*`). |
| `Dockerfile` | Receta de la imagen (Python 3.11-slim + deps + código). |
| `docker-compose.yml` | Orquesta `db` (Postgres) + `web` (Django). |
| `requirements.txt` | Añade `psycopg2-binary` (driver de PostgreSQL). |
| `.env.example` | Referencia de variables de entorno. |

> **Nota de nombres:** el PDF usa `tienda_project`; en este proyecto el paquete del
> proyecto se llama **`Tienda`** (ahí está `wsgi.py`/`settings.py`). Todo ya está
> ajustado a `Tienda`.

---

## A) Prueba local con Docker Compose

Requisito: Docker Desktop instalado.

```bash
# Desde la carpeta de este tutorial
docker compose up -d --build

# Crear las tablas y los datos de prueba DENTRO del contenedor web
docker compose exec web python manage.py migrate
docker compose exec web python manage.py seed_datos

# (opcional) ver que corren los 2 contenedores
docker compose ps
```

Pruebe la API en: `http://localhost:8000/api/v1/comprar/`

Para apagar todo:
```bash
docker compose down            # agregue -v para borrar también el volumen de datos
```

---

## B) Despliegue en AWS EC2 (AWS Academy)

### B.1 Lanzar la instancia
1. AWS Academy → **Start Lab** → consola de AWS → **EC2 → Launch Instance**.
2. **Name:** `Servidor-Django`
3. **OS Image:** Amazon Linux 2023 AMI (Free tier)
4. **Instance Type:** `t2.micro`
5. **Key Pair:** `vockey` (o "Proceed without a key pair" si usará EC2 Instance Connect)
6. **Network Settings:** marque *Allow SSH*, *Allow HTTP* y *Allow HTTPS*.
7. **Launch instance.**

### B.2 Conectarse
Instancia → **Connect** → pestaña **EC2 Instance Connect** → **Connect**.

### B.3 Instalar Git y Docker en la EC2
```bash
sudo dnf update -y
sudo dnf install git docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user
exit                 # cierre y reconecte para aplicar permisos de docker
```

### B.4 Clonar el repo y desplegar  ⚠️ (ajustado a nuestra estructura de carpetas)
```bash
git clone https://github.com/xarqoz/tutoriales-arqsoftware.git
cd tutoriales-arqsoftware/tutorial04        # <- entramos a la carpeta del tutorial

docker compose up -d --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py seed_datos

docker ps                                   # verifique que db y web están "Up"
```
> Si la EC2 no trae `docker compose` (v2), use `docker-compose` (v1).

### B.5 Abrir el puerto 8000 (Security Group)
1. EC2 → **Instances** → su instancia → pestaña **Security** → clic en el Security Group.
2. **Edit inbound rules → Add rule.**
3. **Type:** Custom TCP · **Port range:** `8000` · **Source:** `0.0.0.0/0`
4. **Save rules.**

---

## Evidencia a entregar

Captura del navegador accediendo a:

```
http://<IP-PUBLICA-EC2>:8000/api/v1/comprar/
```

Debe verse la respuesta JSON de la API (la interfaz navegable de DRF) **servida desde AWS**.

> 💡 **Para ahorrar créditos de AWS Academy:** al terminar, ejecute `docker compose down`
> y detenga/termine la instancia EC2.
