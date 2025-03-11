import pandas as pd
from flask import Flask, request, jsonify, send_file, render_template
import io
from config import Config



app = Flask(__name__)

# @app.route('/')
# def index():

# CREAR un producto (INSERT)
@app.route('/productos', methods=['POST'])
def crear_producto():
    data = request.get_json()  # Recibe JSON con nombre, precio y stock
    conn = Config.get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s) RETURNING id",
            (data['nombre'], data['precio'], data['stock'])
        )
        producto_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Producto creado", "id": producto_id}), 201
    return jsonify({"error": "Error al conectar"}), 500

# LEER todos los productos (SELECT)
@app.route('/productos', methods=['GET'])
def obtener_productos():
    conn = Config.get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, precio, stock FROM productos")
        productos = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(productos)
    return jsonify({"error": "Error al conectar"}), 500

# ACTUALIZAR un producto (UPDATE)
@app.route('/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    data = request.get_json()
    conn = Config.get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE productos SET nombre = %s, precio = %s, stock = %s WHERE id = %s",
            (data['nombre'], data['precio'], data['stock'], id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Producto actualizado"})
    return jsonify({"error": "Error al conectar"}), 500

# ELIMINAR un producto (DELETE)
@app.route('/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    conn = Config.get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Producto eliminado"})
    return jsonify({"error": "Error al conectar"}), 500

# CREAR una venta (POST) - Registra una nueva venta
@app.route('/crear_venta', methods=['POST'])
def crear_venta():
    data = request.get_json()  # Recibe JSON con los productos y cantidades
    productos = data.get('productos')  # Lista de productos vendidos
    total_venta = sum([producto['cantidad'] * producto['precio_unitario'] for producto in productos])

    # Conexión a la base de datos
    conn = Config.get_connection()
    if conn:
        cursor = conn.cursor()

        # Insertar la venta en la tabla 'ventas'
        cursor.execute("INSERT INTO ventas (total) VALUES (%s) RETURNING id", (total_venta,))
        venta_id = cursor.fetchone()[0]  # Obtener el ID de la venta

        # Insertar los detalles de la venta en 'detalle_venta'
        for producto in productos:
            cursor.execute("""
                INSERT INTO detalle_venta (venta_id, producto_id, cantidad, precio_unitario, total)
                VALUES (%s, %s, %s, %s, %s)
            """, (venta_id, producto['producto_id'], producto['cantidad'], producto['precio_unitario'], producto['cantidad'] * producto['precio_unitario']))

        conn.commit()  # Confirmar los cambios
        cursor.close()
        conn.close()

        return jsonify({"mensaje": "Venta registrada", "venta_id": venta_id, "total": total_venta}), 201

    return jsonify({"error": "Error al conectar"}), 500

# VER una factura (GET) - Muestra los detalles de una venta
@app.route('/factura/<int:venta_id>', methods=['GET'])
def ver_factura(venta_id):
    conn = Config.get_connection()
    if conn:
        cursor = conn.cursor()

        # Obtener la información de la venta
        cursor.execute("SELECT * FROM ventas WHERE id = %s", (venta_id,))
        venta = cursor.fetchone()

        if not venta:
            return jsonify({"mensaje": "Venta no encontrada"}), 404

        # Obtener los detalles de la venta
        cursor.execute("""
            SELECT p.nombre, dv.cantidad, dv.precio_unitario, dv.total
            FROM detalle_venta dv
            JOIN productos p ON p.id = dv.producto_id
            WHERE dv.venta_id = %s
        """, (venta_id,))
        detalles = cursor.fetchall()

        # Crear la factura
        factura = {
            "id_venta": venta[0],
            "fecha": venta[1],
            "total": venta[2],
            "productos": [{"nombre": detalle[0], "cantidad": detalle[1], "precio_unitario": detalle[2], "total": detalle[3]} for detalle in detalles]
        }

        cursor.close()
        conn.close()

        return jsonify(factura)

    return jsonify({"error": "Error al conectar"}), 500

@app.route('/descargar_reporte_ventas', methods=['GET'])
def descargar_reporte_ventas():
    if request.method == 'GET' and 'download' in request.args:
        # Lógica para generar y descargar el reporte de ventas
        conn = Config.get_connection()

        if not conn:
            return jsonify({"error": "Error al conectar con la base de datos"}), 500
        
        try:
            cursor = conn.cursor()
            cursor.execute(""" 
                SELECT v.id AS venta_id, v.fecha, v.total, 
                       dv.producto_id, dv.cantidad, dv.precio_unitario, dv.total AS subtotal
                FROM ventas v
                JOIN detalle_venta dv ON v.id = dv.venta_id
                ORDER BY v.fecha DESC, v.id;
            """)
            ventas = cursor.fetchall()

            if not ventas:
                return jsonify({"error": "No hay ventas registradas"}), 404
            
            # Crear DataFrame con los datos
            columnas = ["Venta ID", "Fecha", "Total", "Producto ID", "Cantidad", "Precio Unitario", "Subtotal"]
            df = pd.DataFrame(ventas, columns=columnas)

            # Generar archivo Excel en memoria
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            output.seek(0)  # Volver al inicio del buffer

            # Enviar archivo como respuesta
            return send_file(
                output,
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                as_attachment=True,
                download_name="reporte_ventas.xlsx"
            )

        except Exception as e:
            return jsonify({"error": f"Error al generar el reporte: {str(e)}"}), 500

        finally:
            cursor.close()
            conn.close()
    
    # Si no es la solicitud de descarga, simplemente renderizamos el HTML
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)