# Artiko — Fábrica de Hielo (Proyecto listo para Render.com)

## Contenido
- `index.html` — página principal
- `static/` — CSS, JS y assets (logo, favicon)
- `app.py` — servidor Flask que guarda contactos y envía correo vía SMTP
- `requirements.txt` — dependencias
- `.env.example` — variables de entorno de ejemplo
- `data/contacts.csv` — archivo donde se guardan los contactos (se crea automáticamente)

## Preparación local
1. Copia `.env.example` a `.env` y completa las variables (`MAIL_USER`, `MAIL_PASS`, etc.).
2. Crea un entorno virtual e instala dependencias:
```bash
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows
pip install -r requirements.txt
```
3. Ejecuta la app:
```bash
python app.py
```
4. Abre `http://localhost:5000` y prueba el formulario.

## Despliegue en Render.com
1. Sube el repositorio a GitHub (o sube el ZIP directamente a Render).
2. En Render: New → Web Service → conecta el repo o sube ZIP.
3. Runtime: Python 3.x. Build Command: (dejar vacío). Start Command:
```
gunicorn app:app
```
4. En Environment → agrega variables de entorno: `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USER`, `MAIL_PASS`, `MAIL_TO`.
5. Una vez desplegada, en tu proveedor DNS agrega un registro CNAME apuntando el `www` a la URL que Render te provea y una redirección (ALIAS) desde `artiko.mx` a `www.artiko.mx` según tu registrador.

## Notas
- Para enviar correos desde Gmail, usa **App Passwords** (si tienes 2FA) o el SMTP de tu dominio.
- En producción, protege los archivos `data/contacts.csv` (mejor mover a una base de datos).
- Si quieres, puedo subir esto a GitHub y/o generar el ZIP para descarga.
