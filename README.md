# MVP Control de Inventarios - Maestranzas Unidos S.A.

## Instalación

```bash
python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Usuarios de prueba
- admin / adminpass (superusuario)
- gestor / gestpass (Grupo: Gestor)
- comprador / comprpass (Grupo: Comprador)

## Funcionalidades incluidas
- Autenticación y roles
- CRUD Inventario, Proveedores, RecepciónCompra (via Admin)
- Alerta de stock bajo
- Frontend básico en `/`
