# Funcionamiento de la WebApp "Consulta de Stock"

Esta aplicación permite consultar el inventario (stock) de productos desde la base de datos de Microsoft Access (`GESTION.mdb`) desde cualquier dispositivo (incluyendo celulares) conectado a la red local.

## 1. Arquitectura General

La aplicación utiliza la misma arquitectura que la aplicación de entregas:

1. **Frontend (Interfaz Gráfica):** Un archivo HTML (`stock.html`) diseñado con Bootstrap para adaptarse a pantallas de celulares (diseño "Mobile-First").
2. **Backend (Servidor Web):** Un servidor desarrollado en Python usando Flask (`app_stock.py`).
3. **Conector a Base de Datos:** Reutiliza el script de PowerShell (`query_helper.ps1`) para ejecutar las consultas SQL en Access.

## 2. Datos Consultados

La aplicación consulta información de las tablas **GamaDeProducto** y **ClaseDeProducto**:

- **Perno:** Número de código del perno/artículo
- **Descripción:** Tipo o clase de producto (desde ClaseDeProducto)
- **Ext Min / Ext Max:** Espesor mínimo y máximo del producto
- **Stock:** Cantidad actual disponible en inventario
- **Fecha Stock Inicial:** Fecha del último ajuste de inventario

## 3. Funcionalidad Principal

La aplicación ofrece **dos modos de trabajo**:

### Modo Consulta General:
- **Ver Detalle**: Muestra todos los productos que coinciden con el filtro de perno
- **Resumen por Tipo**: Agrupa el stock por clase de producto

### Modo Navegación por Productos (Nuevo):
- **Cargar Lista de Productos**: Obtiene todos los productos vigentes (sin fecha de baja)
- **Navegación Anterior/Siguiente**: Permite revisar el stock de cada producto uno por uno
- **Contador**: Muestra la posición actual (ej: "5/150" significa producto 5 de 150 totales)

### Actualización de Stock:
- **Desde tabla**: Hacer clic en cualquier fila para rellenar automáticamente el formulario
- **Desde navegación**: El producto actual se muestra automáticamente en el formulario
- **Validación**: Confirma antes de actualizar y muestra mensaje de éxito/error

## 4. Flujo de Trabajo Recomendado

1. **Cargar lista**: Hacer clic en "Cargar Lista de Productos"
2. **Navegar**: Usar "Siguiente" para revisar cada producto
3. **Verificar stock**: Comparar con inventario físico
4. **Actualizar si necesario**: Hacer clic en fila → ingresar nuevo stock → actualizar
5. **Continuar**: Repetir para todos los productos

## 5. Datos Consultados

La aplicación consulta información de las tablas **GamaDeProducto**, **ClaseDeProducto** y **Producto**:

- **Perno**: Código del producto
- **Clase**: Tipo de producto (desde ClaseDeProducto)
- **Stock**: Cantidad actual disponible
- **Ext Min/Ext Max**: Espesor mínimo y máximo (con 3 decimales)
- **Fecha Stock Inicial**: Última actualización de inventario

### Productos Vigentes:
Solo se incluyen productos que no tienen fecha de baja en la tabla **Producto**.

## 6. Navegación por Productos (Nueva Funcionalidad)

Esta funcionalidad permite revisar el inventario de manera sistemática, producto por producto:

### Cómo usar la navegación:

1. **Cargar Lista**: Hacer clic en "Cargar Lista de Productos" para obtener todos los productos vigentes
2. **Navegación**: 
   - **Siguiente**: Avanza al siguiente producto
   - **Anterior**: Retrocede al producto anterior
   - **Contador**: Muestra "X/Y" (producto actual / total de productos)
3. **Actualización**: El producto actual se carga automáticamente en el formulario de actualización
4. **Verificación**: Comparar el stock mostrado con el inventario físico

### Beneficios:
- **Control sistemático**: Asegura que no se olvide ningún producto
- **Eficiencia**: Navegación rápida sin necesidad de filtros manuales
- **Actualización directa**: El formulario se rellena automáticamente con el producto actual

| Aspecto | Entregas | Stock |
|---------|----------|-------|
| **Puerto** | 5000 | 5001 |
| **Archivo Python** | app.py | app_stock.py |
| **Template HTML** | index.html | stock.html |
| **Script de inicio** | IniciarServidor.bat | IniciarServidorStock.bat |
| **Tabla Principal** | entregasalcliente | GamaDeProducto |
| **Filtros** | Cliente, Perno, Lista, Fechas | Solo Perno |
| **Acciones** | 3 tipos de resumen | 2 tipos de resumen + Navegación |

## 5. Uso de la Aplicación

### Para ejecutar el servidor:

1. Abrir una terminal en la carpeta `C:\Pescara\IA\WebApp\`
2. Ejecutar `IniciarServidorStock.bat`
3. El servidor iniciará automáticamente en el puerto 5001

### Para acceder desde cualquier dispositivo:

- **En la misma computadora:** `http://localhost:5001`
- **Desde otro dispositivo en la red:** `http://<IP_LOCAL>:5001`
  - Para conocer la IP local, ejecutar en PowerShell: `ipconfig`

### Ejemplo de uso:

1. Ingresar "54" en el campo Perno para buscar todos los pernos que comiencen con esos dígitos
2. Hacer clic en "Ver Detalle" para ver todos los productos encontrados
3. Con los mismos filtros aplicados, hacer clic en "Resumen por Tipo" para ver el stock total por categoría

## 6. Notas Técnicas

- La aplicación utiliza PowerShell 32-bits por la misma razón que la app de entregas (compatibilidad con OLEDB de Access)
- El servidor Waitress se ejecuta en producción para mejor rendimiento y estabilidad
- El puerto 5001 se utiliza para evitar conflictos con la app de entregas (que usa el 5000)
- Las búsquedas de perno son parciales (LIKE '%perno%') para mayor flexibilidad en la búsqueda

## 7. Troubleshooting

### Si la aplicación no conecta a la base de datos:

1. Verificar que `GESTION.mdb` existe en `C:\Pescara\IA\`
2. Verificar que el archivo es accesible y no está abierto en Access
3. Revisar que `query_helper.ps1` existe en `C:\Pescara\IA\WebApp\`

### Si el servidor no inicia:

1. Verificar que Python está instalado: `python --version`
2. Verificar que no hay otro proceso usando el puerto 5001
3. Revisar que el entorno virtual se crea correctamente

