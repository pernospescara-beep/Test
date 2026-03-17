@echo off
rem ------------------------------------------------------------------
rem production startup script – uses waitress instead of Flask builtin
rem ------------------------------------------------------------------

title Servidor de Entregas Movil

echo Iniciando servidor web de Entregas Móvil (modo producción)...
cd /d C:\Pescara\IA\WebApp
call venv\Scripts\activate.bat

rem ensure flask knows we want production behavior (app.py checks this)
set FLASK_ENV=production

rem install waitress if it isn't already present
python -m pip install --upgrade waitress

rem either run the application directly, which will invoke waitress
python app.py

pause
