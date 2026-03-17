@echo off
echo === PRUEBA DEL SISTEMA DE SINCRONIZACION ===
echo.

echo 1. Verificando que el servicio este ejecutandose...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:5002/sync/status' -UseBasicParsing; Write-Host '✓ Servicio activo - Status:' $response.StatusCode } catch { Write-Host '✗ Servicio no responde' }"

echo.
echo 2. Probando sincronizacion forzada...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:5002/sync/force' -Method POST -ContentType 'application/json' -UseBasicParsing; Write-Host '✓ Sincronizacion exitosa - Status:' $response.StatusCode } catch { Write-Host '✗ Error en sincronizacion:' $_.Exception.Message }"

echo.
echo 3. Verificando datos en SQLite...
cd /d "%~dp0"
python -c "
import sqlite3
import os
db_path = 'sync.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM ClaseDeProducto')
    clase_count = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM GamaDeProducto')
    gama_count = cursor.fetchone()[0]
    print(f'✓ ClaseDeProducto: {clase_count} registros')
    print(f'✓ GamaDeProducto: {gama_count} registros')
    conn.close()
else:
    print('✗ Base de datos no encontrada')
"

echo.
echo 4. Verificando programacion automatica...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:5002/sync/status' -UseBasicParsing; $content = $response.Content | ConvertFrom-Json; if ($content.scheduler_running -eq $true) { Write-Host '✓ Scheduler activo' } else { Write-Host '✗ Scheduler inactivo' } } catch { Write-Host '✗ Error al verificar scheduler' }"

echo.
echo === PRUEBA COMPLETADA ===
pause