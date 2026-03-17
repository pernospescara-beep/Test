@echo off
REM Script para iniciar el servidor de Stock en Windows
REM Con soporte para entorno virtual y servidor Waitress en producción

setlocal enabledelayedexpansion

REM Cambiar al directorio de la webapp
cd /d "%~dp0"

REM Crear el entorno virtual si no existe
if not exist "venv" (
    echo Creando entorno virtual...
    python -m venv venv
)

REM Activar el entorno virtual
call venv\Scripts\activate.bat

REM Instalar dependencias
echo Instalando/Actualizando dependencias...
pip install --upgrade flask waitress

REM Configurar variables de entorno
set FLASK_ENV=production

REM Iniciar el servidor con Waitress en el puerto 5001
echo.
echo ==================================================
echo Iniciando servidor de Stock en puerto 5001
echo ==================================================
echo Acceder desde: http://localhost:5001
echo O desde otro dispositivo: http://[IP_LOCAL]:5001
echo.
python -m waitress --port=5001 app_stock:app

pause
