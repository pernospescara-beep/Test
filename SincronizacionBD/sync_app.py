from flask import Flask, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging
from sync_manager import SyncManager
import os

app = Flask(__name__)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Inicializar manager de sincronización
sync_manager = SyncManager()

# Scheduler global
scheduler = BackgroundScheduler()

@app.route('/')
def index():
    return jsonify({
        "message": "Servicio de Sincronización Access → SQLite",
        "status": "running",
        "endpoints": {
            "/sync/force": "POST - Forzar sincronización manual",
            "/sync/status": "GET - Ver estado de sincronización"
        }
    })

@app.route('/sync/force', methods=['POST'])
def force_sync():
    """Endpoint para forzar sincronización manual"""
    try:
        logger.info("Sincronización forzada iniciada")
        sync_manager.sync_all_tables()
        return jsonify({
            "success": True,
            "message": "Sincronización completada exitosamente",
            "status": sync_manager.get_sync_status()
        })
    except Exception as e:
        logger.error(f"Error en sincronización forzada: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/sync/status', methods=['GET'])
def get_status():
    """Obtener estado actual de sincronización"""
    try:
        status = sync_manager.get_sync_status()
        return jsonify({
            "status": status,
            "scheduler_running": scheduler.running
        })
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

def scheduled_sync():
    """Función que se ejecuta cada 5 minutos"""
    try:
        logger.info("Ejecutando sincronización programada")
        sync_manager.sync_all_tables()
    except Exception as e:
        logger.error(f"Error en sincronización programada: {e}")

def start_scheduler():
    """Iniciar el scheduler con sincronización cada 5 minutos"""
    # Agregar job para sincronización cada 5 minutos
    scheduler.add_job(
        func=scheduled_sync,
        trigger=IntervalTrigger(minutes=5),
        id='sync_job',
        name='Sincronización Access → SQLite',
        replace_existing=True
    )

    # Iniciar scheduler
    scheduler.start()
    logger.info("Scheduler iniciado - sincronización cada 5 minutos")

    # Ejecutar sincronización inicial
    try:
        logger.info("Ejecutando sincronización inicial")
        sync_manager.sync_all_tables()
    except Exception as e:
        logger.error(f"Error en sincronización inicial: {e}")

if __name__ == '__main__':
    # Iniciar scheduler al arrancar la app
    start_scheduler()

    # Ejecutar Flask app
    port = int(os.environ.get('PORT', 5002))  # Puerto diferente al de stock (5001)
    logger.info(f"Iniciando servidor de sincronización en puerto {port}")
    app.run(host='0.0.0.0', port=port, debug=False)

    # Al cerrar, detener scheduler
    scheduler.shutdown()