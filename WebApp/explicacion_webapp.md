# Funcionamiento de la WebApp "Entregas Móvil"

Esta aplicación permite consultar la base de datos de Microsoft Access (`GESTION.mdb`) desde cualquier dispositivo (incluyendo celulares) conectado a la red local. A continuación se detalla su funcionamiento y arquitectura.

## 1. Arquitectura General

La aplicación se compone de tres partes principales:

1. **Frontend (Interfaz Gráfica):** Un archivo HTML (`index.html`) diseñado con Bootstrap para adaptarse perfectamente a pantallas de celulares (diseño "Mobile-First").
2. **Backend (Servidor Web):** Un servidor desarrollado en Python usando el framework web **Flask** (`app.py`). Este servidor recibe las peticiones desde la interfaz gráfica.
3. **Conector a Base de Datos:** Un script de PowerShell (`query_helper.ps1`) encargado de ejecutar las consultas SQL en la base de datos Access.

## 2. ¿Por qué se usa PowerShell?

Las bases de datos Access antiguas suelen requerir controladores (drivers) de **32 bits** (Microsoft.Jet.OLEDB.4.0). Si la versión de Python instalada en la computadora es de 64 bits, no puede comunicarse directamente con la base de datos.
Para solucionar esto, Python invoca a la versión de **32 bits de PowerShell** integrada en Windows (ubicada en `SysWOW64`), ejecutando el archivo `query_helper.ps1`. 
PowerShell obtiene los datos, los convierte a formato JSON y se los devuelve a Python, el cual se los entrega finalmente al navegador web.

## 3. Funcionalidad Principal

La WebApp permite consultar las **entregas al cliente**. Para ello, ofrece diversos **filtros** y **tres tipos de reportes**:

### Filtros disponibles:
- **Cliente:** Se puede buscar por código interno o referencia del cliente (ej. 150 o DC760).
- **Perno:** Permite filtrar entregas específicas de un número de perno.
- **Lista:** Permite filtrar por una lista de precios en particular (ej. A, B, etc).
- **Fechas (Desde / Hasta):** Establece un rango de fechas para limitar los resultados mostrados.

### Tipos de consultas:
1. **Ver Detalle (Botón Azul):** 
   Muestra un listado detallado (con un límite de 300 resultados para no saturar el celular) de las entregas que coinciden con los filtros aplicados. Muestra campos como Fecha, Cliente, Perno, Lista, Cantidad, Precio y el Total (Cantidad x Precio).
2. **Resumir por Perno (Botón Verde):** 
   Agrupa los resultados según el número de perno especificado, sumando las cantidades totales y el valor económico total para cada uno.
3. **Resumir Cli+Perno (Botón Celeste):** 
   Un nivel de detalle intermedio. Agrupa y suma las cantidades y los montos totales de los artículos, separados por cliente y por número de perno.

## 4. Uso de la Aplicación
Para que la aplicación funcione, siempre debe estar ejecutándose el servidor en la computadora principal (ejecutando el archivo `IniciarServidor.bat`).

> **Nota sobre producción:**  El servidor incorporado de Flask sólo debe usarse para pruebas. En entornos de producción en Windows se recomienda un servidor WSGI estable como **Waitress**. El lote `IniciarServidor.bat` ahora activa el entorno virtual, fija `FLASK_ENV=production` e instala/ejecuta Waitress para proporcionar un rendimiento más robusto y seguro.

Cualquier persona conectada al WiFi puede ingresar a la dirección IP local de la computadora seguida del puerto `:5000` (Ej: `http://192.168.0.38:5000`) para usar el sistema.
