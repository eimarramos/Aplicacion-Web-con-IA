# Proyecto Flask

Prototipo funcional estilo Instagram con Flask y Python.

Funciones incluidas:

- Crear publicaciones (texto obligatorio, URL de imagen opcional)
- Visualizar publicaciones en un feed
- Eliminar publicaciones

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
- models.py
- forms.py
- templates/index.html
- tests/test_app.py
