# Sistema de Sincronización Access → SQLite

Este sistema sincroniza automáticamente datos desde Microsoft Access (GESTION.mdb) hacia SQLite para preparar la migración a web.

## 🚀 Instalación y Uso

### 1. Instalar dependencias
```bash
cd SincronizacionBD
pip install -r requirements_sync.txt
```

### 2. Ejecutar el servicio de sincronización
```bash
python sync_app.py
```

### 3. Probar el sistema
```bash
ProbarSincronizacion.bat
```

El servicio se ejecutará en **http://localhost:5002**

## 📋 Funcionalidades

### ✅ Sincronización automática
- **Cada 5 minutos**: sincroniza automáticamente todas las tablas configuradas
- **Inicial**: al iniciar el servicio, ejecuta una sincronización completa

### ✅ Sincronización manual
```bash
curl -X POST http://localhost:5002/sync/force
```

### ✅ Estado de sincronización
```bash
curl http://localhost:5002/sync/status
```

## 📊 Tablas sincronizadas

Actualmente sincroniza estas tablas:

- **ClaseDeProducto**: Códigos, descripciones y orden de clases (33 registros)
- **GamaDeProducto**: Stock, dimensiones y fechas por producto (4,223 registros)
- **Producto**: ⚠️ Temporalmente deshabilitado - problemas de consulta en Access

### Nota sobre tabla Producto
La tabla Producto está deshabilitada porque las consultas directas fallan con error "No se han especificado valores para algunos de los parámetros requeridos". Esto sugiere que puede ser una vista o query parametrizada en Access. La funcionalidad actual de la app no requiere esta tabla.

## 🔧 Configuración

### Agregar nuevas tablas
Editar `mappers.py` y agregar entrada en `TABLE_MAPPERS`:

```python
'NuevaTabla': {
    'source_query': "SELECT * FROM NuevaTabla",
    'schema': """
        CREATE TABLE IF NOT EXISTS NuevaTabla (
            id INTEGER PRIMARY KEY,
            nombre TEXT
        );
    """,
    'columns': ['id', 'nombre']
}
```

### Cambiar frecuencia de sincronización
En `sync_app.py`, modificar:
```python
trigger=IntervalTrigger(minutes=5),  # Cambiar a hours=1, etc.
```

## 📁 Archivos generados

- `sync.db`: Base de datos SQLite con datos sincronizados
- `sync.log`: Log de todas las sincronizaciones

## 🔄 Próximos pasos para web

1. **Modificar app_stock.py** para leer de SQLite en lugar de Access
2. **Migrar a PostgreSQL** cuando sea necesario
3. **Implementar sincronización incremental** para mejor performance

## 🛠️ Solución de problemas

- **Error de conexión a Access**: verificar que el archivo GESTION.mdb existe y no está en uso
- **Error de permisos SQLite**: verificar permisos de escritura en la carpeta
- **Scheduler no funciona**: verificar que APScheduler esté instalado correctamente
- **Tabla Producto deshabilitada**: consultas directas fallan en Access. Puede ser una vista parametrizada. La app funciona sin ella.