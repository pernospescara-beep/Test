[CmdletBinding()]
param([string]$sql)

$ErrorActionPreference = "Stop"

try {
    # Usamos explícitamente el proveedor de 32 bits porque este script se llamará desde SysWOW64
    $conn = New-Object System.Data.OleDb.OleDbConnection("Provider=Microsoft.Jet.OLEDB.4.0;Data Source=C:\Pescara\IA\GESTION.mdb;")
    $conn.Open()
    $cmd = $conn.CreateCommand()
    $cmd.CommandText = $sql
    
    $da = New-Object System.Data.OleDb.OleDbDataAdapter($cmd)
    $dt = New-Object System.Data.DataTable
    $da.Fill($dt) | Out-Null
    
    if ($dt.Rows.Count -eq 0) {
        Write-Output "[]"
        exit
    }
    
    $results = @()
    foreach ($row in $dt.Rows) {
        # Armar un hashtable clásico para máxima compatibilidad con versiones antiguas
        $dict = @{}
        foreach ($col in $dt.Columns) {
            $val = $row[$col.ColumnName]
            if ([DBNull]::Value.Equals($val)) {
                $val = $null
            } elseif ($val -is [DateTime]) {
                $val = $val.ToString("yyyy-MM-ddTHH:mm:ss")
            }
            $dict[$col.ColumnName] = $val
        }
        $results += $dict
    }

    # Output en formato JSON. Se configurará Depth para que PowerShell convierta la lista de objetos correctamente
    $json = $results | ConvertTo-Json -Depth 5 -Compress
    
    # Nos aseguramos la codificación UTF8 para la salida
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    Write-Output $json

} catch {
    # Imprimimos y salimos con error
    [Console]::Error.WriteLine($_.Exception.Message)
    exit 1
} finally {
    if ($conn -and $conn.State -eq 'Open') { $conn.Close() }
}
