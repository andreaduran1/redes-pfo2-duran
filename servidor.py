import sqlite3
from flask import Flask, request, jsonify, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash

# Inicialización de la aplicación Flask
app = Flask(__name__)
DB_NAME = "test.db"

def init_db():
    """
    Crea la tabla de usuarios si aún no existe.
    Garantiza que la columna usuario sea única para evitar duplicados.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/registro", methods=["POST"])
def registro():
    """
    Endpoint para registrar nuevas cuentas.
    1. Lee el cuerpo JSON enviado por el cliente.
    2. Valida la presencia de 'usuario' y 'contraseña'.
    3. Hashea la contraseña con una sal criptográfica.
    4. Guarda el registro en la base de datos o retorna 409 si ya existe.
    """
    datos = request.get_json(silent=True) or {}
    usuario = datos.get("usuario")
    contrasena = datos.get("contraseña")

    if not usuario or not contrasena:
        return jsonify({"error": "Faltan campos requeridos"}), 400

    hash_pw = generate_password_hash(contrasena)

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)", (usuario, hash_pw))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "El usuario ya existe"}), 409

@app.route("/login", methods=["POST"])
def login():
    """
    Endpoint para autenticar credenciales.
    1. Obtiene usuario y contraseña desde la petición JSON.
    2. Busca el hash almacenado para ese nombre de usuario en SQLite.
    3. Compara el hash con la contraseña ingresada de forma segura.
    4. Retorna éxito con la ruta de acceso o error 401 si falla.
    """
    datos = request.get_json(silent=True) or {}
    usuario = datos.get("usuario")
    contrasena = datos.get("contraseña")

    if not usuario or not contrasena:
        return jsonify({"error": "Faltan campos requeridos"}), 400

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT contrasena FROM usuarios WHERE usuario = ?", (usuario,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado and check_password_hash(resultado[0], contrasena):
        return jsonify({"mensaje": "Inicio de sesión exitoso", "acceso": "/tareas"}), 200

    return jsonify({"error": "Credenciales inválidas"}), 401

@app.route("/tareas", methods=["GET"])
def tareas():
    """
    Endpoint que sirve la interfaz de bienvenida.
    Renderiza una plantilla HTML en memoria informando el acceso a las tareas.
    """
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head><title>Gestion de Tareas</title></head>
    <body style="font-family: sans-serif; text-align: center; margin-top: 50px;">
        <h1>Bienvenido/a a la Gestión de Tareas</h1>
        <p>Sesión iniciada correctamente.</p>
    </body>
    </html>
    """
    return render_template_string(html), 200

if __name__ == "__main__":
    init_db()
    app.run(port=5000, debug=True)