# WebApp de Consultas GESTION.mdb

Conjunto de aplicaciones web para consultar la base de datos `GESTION.mdb` desde dispositivos conectados a la red local (incluyendo celulares).

## Aplicaciones Disponibles

### 1. Consulta de Entregas (Puerto 5000)
**Archivo principal:** `app.py` | **Template:** `templates/index.html`  
**Inicio:** Ejecutar `IniciarServidor.bat`

Consulta entregas realizadas al cliente con filtros por:
- Cliente (código o referencia)  
- Perno
- Lista de precios
- Rango de fechas

**Características:** 3 tipos de reportes (Detalle, Resumen por Perno, Resumen Cliente+Perno)

[Ver documentación completa](explicacion_webapp.md)

---

### 2. Consulta de Stock (Puerto 5001) - ⭐ NUEVO
**Archivo principal:** `app_stock.py` | **Template:** `templates/stock.html`  
**Inicio:** Ejecutar `IniciarServidorStock.bat`

Consulta el inventario de productos con información de:
- Número de perno
- Tipo/Clase de producto  
- Espesor mínimo y máximo
- Stock disponible
- Fecha del último ajuste

**Características:** 
- Filtro por perno (búsqueda parcial)
- 2 tipos de reportes (Detalle, Resumen por Tipo)
- Resaltado visual de stock bajo (<10) y sin inventario (=0)

[Ver documentación completa](explicacion_webapp_stock.md)

---

## Instalación Rápida

### Prerrequisitos
- Python 3.7+ instalado
- Base de datos `GESTION.mdb` en `C:\Pescara\IA\`

### Primeros pasos

1. **Primera vez:** Ejecutar cualquiera de los scripts `.bat`
   - `IniciarServidor.bat` - Para la app de entregas
   - `IniciarServidorStock.bat` - Para la app de stock

2. Los scripts automáticamente:
   - Crean un entorno virtual (si no existe)
   - Instalan las dependencias necesarias
   - Inician el servidor

---

## Acceso a las Aplicaciones

| Aplicación | Ubicación Local | Red Local |
|------------|-----------------|-----------|
| **Entregas** | http://localhost:5000 | http://`<IP>`:`5000` |
| **Stock** | http://localhost:5001 | http://`<IP>`:`5001` |

Para encontrar tu IP local, ejecuta en PowerShell:
```powershell
ipconfig
```
Busca la dirección bajo "Dirección IPv4" (típicamente 192.168.x.x)

---

## Arquitectura Técnica

Ambas aplicaciones utilizan:
- **Frontend:** HTML + Bootstrap 5 (responsive mobile-first)
- **Backend:** Flask (Python web framework)
- **Base de Datos:** Microsoft Access (.mdb) vía PowerShell 32-bits
- **Servidor:** Waitress (en producción)

### Diagrama de flujo
```
Navegador (celular/PC)
    ↓
HTML/JavaScript (Frontend)
    ↓
Flask (Python Backend) - app.py o app_stock.py
    ↓
PowerShell 32-bits (query_helper.ps1)
    ↓
Microsoft Jet.OLEDB.4.0 Driver
    ↓
GESTION.mdb (Base de Datos Access)
```

---

## Archivos de Proyecto

```
WebApp/
├── app.py                          # Backend entregas
├── app_stock.py                    # Backend stock (NUEVO)
├── query_helper.ps1                # Script PowerShell para consultas DB
├── IniciarServidor.bat             # Iniciador entregas
├── IniciarServidorStock.bat        # Iniciador stock (NUEVO)
├── requirements.txt                # Dependencias Python
├── explicacion_webapp.md           # Docs entregas
├── explicacion_webapp_stock.md     # Docs stock (NUEVO)
├── README.md                       # Este archivo
└── templates/
    ├── index.html                  # Frontend entregas
    └── stock.html                  # Frontend stock (NUEVO)
```

---

## Solución de Problemas

### La app no conecta a la BD
- ✓ Verificar que `GESTION.mdb` existe en `C:\Pescara\IA\`
- ✓ Cerrar la BD si está abierta en Access
- ✓ Verificar permisos de lectura en el archivo

### El servidor no inicia
- ✓ Verificar: `python --version`
- ✓ Comprobar que el puerto (5000 o 5001) no esté en uso
- ✓ Ejecutar CMD como administrador

### Búsquedas lentasLlenador
- ✓ Las búsquedas pueden ser lentas en BD grandes (normal)
- ✓ Usar filtros más específicos para acelerar

---

## Desarrollo Futuro

Posibles mejoras:
- [ ] Interfaz unificada para ambas apps
- [ ] Búsqueda avanzada por múltiples criterios
- [ ] Exportar resultados a Excel/PDF
- [ ] Caché de datos para búsquedas frecuentes
- [ ] Autenticación de usuarios

---

## Licencia

Desarrollo interno para Pescara IA

**Última actualización:** Marzo 2026
