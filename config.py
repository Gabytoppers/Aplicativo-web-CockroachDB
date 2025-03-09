import psycopg2

class Config:
    # Configuración de la base de datos
    DB_HOST = "vain-impala-8806.j77.aws-us-east-1.cockroachlabs.cloud"  # Cambia esto con tu host de CockroachDB
    DB_PORT = "26257"  # Por defecto para CockroachDB
    DB_NAME = "defaultdb"  # Tu nombre de base de datos
    DB_USER = "Gabriela"  # Tu usuario
    DB_PASSWORD = "tAIVqRV6v15EGtQLydz33Q"  # Tu contraseña

    @staticmethod
    def get_connection():
        try:
            # Conexión a la base de datos
            connection = psycopg2.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                database=Config.DB_NAME,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD
            )
            print("Conexión exitosa a la base de datos.")
            return connection
        except Exception as e:
            print(f"Error de conexión a la base de datos: {e}")
            return None

# Ejecutar la prueba de conexión
if __name__ == "__main__":
    connection = Config.get_connection()
    if connection:
        print("Operación de conexión completada correctamente.")
        # Cerrar la conexión después de la prueba
        connection.close()

