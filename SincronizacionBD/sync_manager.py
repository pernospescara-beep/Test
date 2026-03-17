import logging
from datetime import datetime
import os
from db_config import execute_access_query, execute_sqlite_query
from mappers import TABLE_MAPPERS

# Configurar logging
logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), 'sync.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SyncManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def initialize_sqlite_schema(self):
        """Crear tablas en SQLite si no existen"""
        try:
            for table_name, config in TABLE_MAPPERS.items():
                self.logger.info(f"Inicializando esquema para tabla {table_name}")
                # Ejecutar cada statement SQL por separado
                schema_statements = [stmt.strip() for stmt in config['schema'].split(';') if stmt.strip()]
                for statement in schema_statements:
                    execute_sqlite_query(statement, fetch=False)
            self.logger.info("Esquemas inicializados correctamente")
        except Exception as e:
            self.logger.error(f"Error inicializando esquemas: {e}")
            raise

    def sync_table(self, table_name):
        """Sincronizar una tabla específica"""
        try:
            config = TABLE_MAPPERS[table_name]
            self.logger.info(f"Iniciando sincronización de tabla {table_name}")

            # Leer datos de Access
            columns, data = execute_access_query(config['source_query'])
            self.logger.info(f"Leídos {len(data)} registros de Access para {table_name}")

            # Limpiar tabla en SQLite
            execute_sqlite_query(f"DELETE FROM {table_name}", fetch=False)

            # Insertar datos en SQLite
            if data:
                placeholders = ', '.join(['?'] * len(config['columns']))
                insert_sql = f"INSERT INTO {table_name} ({', '.join(config['columns'])}) VALUES ({placeholders})"

                for row in data:
                    values = [row.get(col) for col in config['columns']]
                    execute_sqlite_query(insert_sql, params=values, fetch=False)

            self.logger.info(f"Sincronización completada para {table_name}: {len(data)} registros")

        except Exception as e:
            self.logger.error(f"Error sincronizando tabla {table_name}: {e}")
            raise

    def sync_all_tables(self):
        """Sincronizar todas las tablas configuradas"""
        start_time = datetime.now()
        self.logger.info("=== Iniciando sincronización completa ===")

        try:
            # Inicializar esquemas si es necesario
            self.initialize_sqlite_schema()

            # Sincronizar cada tabla
            for table_name in TABLE_MAPPERS.keys():
                self.sync_table(table_name)

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            self.logger.info(f"=== Sincronización completada en {duration:.2f} segundos ===")

        except Exception as e:
            self.logger.error(f"=== Error en sincronización completa: {e} ===")
            raise

    def get_sync_status(self):
        """Obtener estado actual de las tablas sincronizadas"""
        status = {}
        try:
            for table_name in TABLE_MAPPERS.keys():
                columns, data = execute_sqlite_query(f"SELECT COUNT(*) as count FROM {table_name}")
                count = data[0]['count'] if data else 0
                status[table_name] = count
        except Exception as e:
            self.logger.error(f"Error obteniendo status: {e}")
            status['error'] = str(e)

        return status