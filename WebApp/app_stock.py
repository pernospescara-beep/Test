
import os
import json
import subprocess
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

PS_SCRIPT = r"C:\Pescara\IA\WebApp\query_helper.ps1"
PS_EXE = r"C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe"

def execute_query(sql):
    try:
        # Ejecutamos PowerShell 32-bits pasando nuestra query SQL usando el charset por defecto del SO o latin-1 para prever ñ
        result = subprocess.run(
            [PS_EXE, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", PS_SCRIPT, sql],
            capture_output=True,
            text=True,
            encoding='latin-1',
            errors='replace'
        )
        
        if result.returncode != 0:
            raise Exception(f"Fallo en PS 32-bit: {result.stderr.strip()}")
            
        out = result.stdout.strip()
        if not out:
            return [], []
            
        # A veces PS imprime advertencias antes del JSON. Limpiamos buscando el corchete.
        if out.find("[") != -1:
            out = out[out.find("["):]
            
        data = json.loads(out)
        if not isinstance(data, list):
            data = [data]
            
        if len(data) > 0:
            # Filtrar columnas si hay basurita
            columns = list(data[0].keys())
            return columns, data
        else:
            return [], []
    except Exception as e:
        raise e

@app.route('/')
def index():
    return render_template('stock.html')

@app.route('/api/query', methods=['POST'])
def query_db():
    data = request.json
    action = data.get('action')
    
    # Filtros
    where_clauses = []
    
    # A veces el perno llega como número desde el cliente (JSON), así que forzamos a string
    perno = str(data.get('perno') or "").strip()
    if perno:
        # where_clauses.append(f"GamaDeProducto.Perno LIKE '%{perno}%'")
        where_clauses.append(f"GamaDeProducto.Perno = {perno}")
    where_sql = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""
    
    if action == 'listar':
        sql = f"""SELECT GamaDeProducto.Perno, ClaseDeProducto.Descripcion AS Clase, 
                         GamaDeProducto.Stock, GamaDeProducto.DEmin AS [Ext Min], 
                         GamaDeProducto.DEmax AS [Ext Max], GamaDeProducto.fechaStockInicial
                  FROM GamaDeProducto INNER JOIN ClaseDeProducto ON GamaDeProducto.Tipo = ClaseDeProducto.Codigo 
                  {where_sql} ORDER BY ClaseDeProducto.Orden"""
    elif action == 'resumen_stock':
        sql = f"""SELECT ClaseDeProducto.Descripcion AS Clase, SUM(GamaDeProducto.Stock) AS StockTotal
                  FROM GamaDeProducto INNER JOIN ClaseDeProducto ON GamaDeProducto.Tipo = ClaseDeProducto.Codigo 
                  {where_sql} GROUP BY ClaseDeProducto.Descripcion, ClaseDeProducto.Orden ORDER BY ClaseDeProducto.Orden"""
    else:
        return jsonify({"error": "Acción no válida"})

    try:
        columns, results = execute_query(sql)
        return jsonify({"columns": columns, "data": results})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/get-clases', methods=['GET'])
def get_clases():
    """Obtener todas las clases de producto para cargar en el dropdown"""
    sql = "SELECT Codigo, Descripcion FROM ClaseDeProducto ORDER BY Orden"
    
    try:
        columns, results = execute_query(sql)
        return jsonify({"data": results})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/get-tipo-codigo', methods=['POST'])
def get_tipo_codigo():
    """Obtener el código (Tipo) de ClaseDeProducto según su Descripción"""
    data = request.json
    descripcion = (data.get('descripcion') or "").strip()
    
    if not descripcion:
        return jsonify({"error": "Descripción es requerida"})
    
    sql = f"SELECT Codigo FROM ClaseDeProducto WHERE Descripcion = '{descripcion}'"
    
    try:
        columns, results = execute_query(sql)
        if results and len(results) > 0:
            codigo = results[0].get('Codigo')
            return jsonify({"codigo": codigo})
        else:
            return jsonify({"error": f"No se encontró clase con descripción '{descripcion}'"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/get-productos-vigentes', methods=['GET'])
def get_productos_vigentes():
    """Obtener todos los códigos de productos vigentes"""
    sql = """SELECT DISTINCT GamaDeProducto.Perno
             FROM GamaDeProducto INNER JOIN Producto ON GamaDeProducto.Perno = Producto.CODIGO
             WHERE (((Producto.FECHABAJA) Is Null))
             ORDER BY GamaDeProducto.Perno"""
    
    try:
        columns, results = execute_query(sql)
        productos = [row['Perno'] for row in results]
        return jsonify({"productos": productos})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/get-stock-producto', methods=['POST'])
def get_stock_producto():
    """Obtener el stock actual de un producto específico"""
    data = request.json
    # El perno puede llegar como número desde el frontend, asegurar que sea texto
    perno = str(data.get('perno') or "").strip()
    
    if not perno:
        return jsonify({"error": "Perno es requerido"})
    
    # Asegurar que el perno se use con el mismo tipo de datos que en la base
    perno_sql = perno if perno.isdigit() else f"'{perno}'"

    sql = f"""SELECT GamaDeProducto.Perno, ClaseDeProducto.Descripcion AS Clase, 
                     GamaDeProducto.Stock, GamaDeProducto.DEmin AS [Ext Min], 
                     GamaDeProducto.DEmax AS [Ext Max], GamaDeProducto.fechaStockInicial
              FROM GamaDeProducto INNER JOIN ClaseDeProducto ON GamaDeProducto.Tipo = ClaseDeProducto.Codigo 
              WHERE GamaDeProducto.Perno = {perno_sql}
              ORDER BY ClaseDeProducto.Orden"""
    
    try:
        columns, results = execute_query(sql)
        return jsonify({"columns": columns, "data": results})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/update-stock', methods=['POST'])
def update_stock():
    data = request.json
    # Asegurar que valores numéricos llegados como JSON se procesen como strings
    perno = str(data.get('perno') or "").strip()
    tipo_codigo = str(data.get('tipo') or "").strip()  # Ahora recibe el código directamente
    stock = data.get('stock')
    
    if not perno or not tipo_codigo or stock is None:
        return jsonify({"error": "Perno, Tipo y Stock son requeridos"})
    
    if not isinstance(stock, int) or stock < 0:
        return jsonify({"error": "La cantidad de stock debe ser un número no negativo"})
    
    # Intentar convertir valores a números para que coincidan con Access
    try:
        perno_num = int(perno) if perno.isdigit() else f"'{perno}'"
        tipo_num = int(tipo_codigo) if tipo_codigo.isdigit() else f"'{tipo_codigo}'"
    except:
        perno_num = f"'{perno}'"
        tipo_num = f"'{tipo_codigo}'"
    
    # Actualizar usando código de tipo directamente
    sql = f"""UPDATE GamaDeProducto
              SET Stock = {stock}, fechaStockInicial = NOW()
              WHERE Perno = {perno_num}
                AND Tipo = {tipo_num}"""
    
    try:
        result = subprocess.run(
            [PS_EXE, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", PS_SCRIPT, sql],
            capture_output=True,
            text=True,
            encoding='latin-1',
            errors='replace'
        )
        
        if result.returncode != 0:
            raise Exception(f"Error al actualizar: {result.stderr.strip()}")
        
        return jsonify({"success": True, "message": f"Stock del perno {perno} actualizado a {stock}"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    env = os.environ.get('FLASK_ENV', '').lower()
    if env == 'production':
        from waitress import serve
        # bind to all interfaces on port 5001 para no conflictuar con la otra app
        serve(app, host='0.0.0.0', port=5001)
    else:
        # development server with reloader/debugger
        app.run(host='0.0.0.0', port=5001, debug=True)
