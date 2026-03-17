@echo off
REM Script para iniciar el servicio de sincronización
REM Sincroniza Access → SQLite cada 5 minutos

echo Iniciando servicio de sincronización Access → SQLite...
cd /d "%~dp0"

REM Activar entorno virtual si existe
if exist "..\WebApp\venv" (
    call ..\WebApp\venv\Scripts\activate.bat
)

REM Instalar dependencias si no están instaladas
pip install -r requirements_sync.txt

REM Ejecutar el servicio
python sync_app.py