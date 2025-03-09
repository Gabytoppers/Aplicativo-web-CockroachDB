from flask import Flask, request, jsonify
from config import Config

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
