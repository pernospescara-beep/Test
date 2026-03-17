# Configuración de tablas a sincronizar
# Cada tabla tiene: nombre, query de origen, esquema de destino

TABLE_MAPPERS = {
    'ClaseDeProducto': {
        'source_query': "SELECT Codigo, Descripcion, Orden FROM ClaseDeProducto",
        'schema': """
            CREATE TABLE IF NOT EXISTS ClaseDeProducto (
                Codigo INTEGER PRIMARY KEY,
                Descripcion TEXT NOT NULL,
                Orden INTEGER
            );
            CREATE INDEX IF NOT EXISTS idx_clase_descripcion ON ClaseDeProducto(Descripcion);
        """,
        'columns': ['Codigo', 'Descripcion', 'Orden']
    },

    # 'Producto': {  # Temporalmente deshabilitado por error en Access
    #     'source_query': "SELECT CODIGO, DESCRIPCION FROM Producto",
    #     'schema': """
    #         CREATE TABLE IF NOT EXISTS Producto (
    #             CODIGO TEXT PRIMARY KEY,
    #             DESCRIPCION TEXT
    #         );
    #         CREATE INDEX IF NOT EXISTS idx_producto_codigo ON Producto(CODIGO);
    #     """,
    #     'columns': ['CODIGO', 'DESCRIPCION']
    # },

    'GamaDeProducto': {
        'source_query': """
            SELECT Perno, Tipo, Stock, DEmax, DEmin, fechaStockInicial
            FROM GamaDeProducto
        """,
        'schema': """
            CREATE TABLE IF NOT EXISTS GamaDeProducto (
                Perno TEXT,
                Tipo INTEGER,
                Stock INTEGER DEFAULT 0,
                DEmax REAL,
                DEmin REAL,
                fechaStockInicial TEXT,
                PRIMARY KEY (Perno, Tipo)
            );
            CREATE INDEX IF NOT EXISTS idx_gama_perno ON GamaDeProducto(Perno);
            CREATE INDEX IF NOT EXISTS idx_gama_tipo ON GamaDeProducto(Tipo);
        """,
        'columns': ['Perno', 'Tipo', 'Stock', 'DEmax', 'DEmin', 'fechaStockInicial']
    }
}

# Para agregar nuevas tablas en el futuro, solo agregar entrada aquí
# Ejemplo:
# 'NuevaTabla': {
#     'source_query': "SELECT * FROM NuevaTabla",
#     'schema': """
#         CREATE TABLE IF NOT EXISTS NuevaTabla (
#             id INTEGER PRIMARY KEY,
#             nombre TEXT
#         );
#     """,
#     'columns': ['id', 'nombre']
# }