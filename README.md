# Proyecto Flask

Prototipo funcional estilo Instagram con Flask y Python.

Funciones incluidas:

- Registro e inicio/cierre de sesion de usuarios
- Crear publicaciones (texto obligatorio, URL de imagen opcional)
- Visualizar publicaciones en un feed publico
- Eliminar publicaciones propias
- Dar y quitar me gusta (toggle)
- Comentar publicaciones
- Eliminar comentarios (autor del comentario o autor del post)

## Requisitos

- Python 3.10+

## Lista de comandos (PowerShell)

1. Crear entorno virtual:

```powershell
python -m venv .venv
```

2. Activar entorno virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

3. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

4. Ejecutar la aplicación:

```powershell
python app.py
```

5. Abrir en el navegador:

- http://127.0.0.1:5000/

6. Ejecutar pruebas:

```powershell
pytest
```

## Comandos rápidos

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

## Estructura principal

- app.py
- config.py
- extensions.py
- models.py
- forms.py
- routes/auth.py
- routes/feed.py
- routes/social.py
- templates/base.html
- templates/auth/login.html
- templates/auth/register.html
- templates/components/post_card.html
- templates/components/comment_list.html
- templates/index.html
- tests/test_app.py
