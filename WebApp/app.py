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
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def query_db():
    data = request.json
    action = data.get('action')
    
    # Filtros
    where_clauses = []
    
    cliente = (data.get('cliente') or "").strip().replace("'", "''")
    if cliente:
        if cliente.isdigit():
            where_clauses.append(f"(cliente = {cliente} OR codcli LIKE '%{cliente}%')")
        else:
            where_clauses.append(f"codcli LIKE '%{cliente}%'")
            
    perno = (data.get('perno') or "").strip()
    if perno and perno.isdigit():
        where_clauses.append(f"perno = {perno}")
            
    lista = (data.get('lista') or "").strip().replace("'", "''")
    if lista:
        where_clauses.append(f"lista LIKE '%{lista}%'")
        
    fecha_desde = (data.get('fechaDesde') or "").strip()
    if fecha_desde:
        where_clauses.append(f"Fecha >= #{fecha_desde}#")
        
    fecha_hasta = (data.get('fechaHasta') or "").strip()
    if fecha_hasta:
        where_clauses.append(f"Fecha <= #{fecha_hasta} 23:59:59#")
        
    where_sql = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""
    
    if action == 'detalle':
        sql = f"SELECT TOP 300 Fecha, cliente AS CodCliente, codcli AS RefCliente, perno AS Perno, lista AS Lista, Cantidad, Pedido, Lote, precioestimado AS PrecioEst, (Cantidad * precioestimado) AS TotalMonto FROM entregasalcliente {where_sql} ORDER BY Fecha DESC"
    elif action == 'resumen_perno':
        sql = f"SELECT perno AS Perno, SUM(Cantidad) AS CantidadTotal, SUM(Cantidad * precioestimado) as MontoTotal FROM entregasalcliente {where_sql} GROUP BY perno ORDER BY SUM(Cantidad) DESC"
    elif action == 'resumen_cliente_perno':
        sql = f"SELECT cliente AS CodCliente, codcli AS RefCliente, perno AS Perno, SUM(Cantidad) AS CantidadTotal, SUM(Cantidad * precioestimado) as MontoTotal FROM entregasalcliente {where_sql} GROUP BY cliente, codcli, perno ORDER BY cliente, SUM(Cantidad) DESC"
    else:
        return jsonify({"error": "Acción no válida"})

    try:
        columns, results = execute_query(sql)
        return jsonify({"columns": columns, "data": results})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    # In development we use Flask's built-in server (with debug enabled for convenience),
    # but this is **not** appropriate for production. On Windows the recommended
    # production WSGI server is *waitress* (pure‑Python, easy to install).
    #
    # Install it in the virtualenv with:
    #     pip install waitress
    #
    # You can either set the environment variable FLASK_ENV=production
    # before launching `python app.py` or simply call this script directly –
    # the check below will pick the right server.
    env = os.environ.get('FLASK_ENV', '').lower()
    if env == 'production':
        from waitress import serve
        # bind to all interfaces on port 5000
        serve(app, host='0.0.0.0', port=5000)
    else:
        # development server with reloader/debugger
        app.run(host='0.0.0.0', port=5000, debug=True)

