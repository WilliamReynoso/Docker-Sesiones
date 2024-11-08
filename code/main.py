import os
import psycopg2
import bcrypt
from psycopg2 import sql
from flask import Flask, request, send_from_directory, session, redirect, url_for, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')  # clave secreta definida en env

UPLOAD_FOLDER = "/uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
# Verificar si el archivo tiene una extension permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Configuracion de Flask-Limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["15 per day", "10 per hour"],  # Límite global (ejemplo: 10 peticiones por hora)
    headers_enabled=os.getenv("RATELIMIT_HEADERS_ENABLED", "true").lower() in ["true", "1"]
)

# Configuracion de la conexion a la base de datos
def get_db_connection():
    connection = psycopg2.connect(
        host="db",
        database=os.getenv("POSTGRES_DB","none"),
        user=os.getenv("POSTGRES_USER", "none"),
        password=os.getenv("POSTGRES_PASSWORD", "none")
    )
    return connection

# Decorador para verificar autenticacion
# Flask ejecuta wrap antes de llamar a protected_route.
# wrap verifica si el usuario esta autenticado. Si es asi llama a protected_route, si no, redirige al usuario a la pagina de login.
def login_required(f):
    def wrap(*args, **kwargs):
        if not session.get('authenticated'):
            return {"error": "usuario no authenticado"}
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

#funcion para registrar usuarios con contraseña encriptada
def register_user(username, password, first_name, last_name, email, device):
    # Generar un salt y encriptar la contraseña
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, first_name, last_name, email, device) VALUES (%s, %s, %s, %s, %s, %s)",
            (username, hashed_password, first_name, last_name, email, device)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Usuario registrado exitosamente"}
    except Exception as e:
        return {"error": str(e)}

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    device = request.form['device']

    # Validar que todos los campos esten presentes
    if not username or not first_name or not last_name or not email or not password or not device:
        return {"error": "todos los campos deben estar estar presentes"}

    # Verificar si el nombre de usuario o correo ya existen
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        return {"error": "El nombre de usuario o email ya estan registrados."}

    # Encriptar la contraseña
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insertar los datos del nuevo usuario en la base de datos
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (username, first_name, last_name, email, password, device)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (username, first_name, last_name, email, hashed_password.decode('utf-8'), device))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Usuario registrado exitosamente."}
    except Exception as e:
        return {f"Error al registrar el usuario: {str(e)}"}

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    # Verificar el usuario con la base de datos o sistema de autenticacion
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        
        if result is None:
            return jsonify({"error": "Usuario no encontrado"}), 404

        hashed_password = result[0]

        # Verificar la contraseña encriptada
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            session['authenticated'] = True
            session['username'] = username
            return jsonify({"message": "Login exitoso"}), 200
        else:
            return jsonify({"error": "Contraseña incorrecta"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/protected')
@login_required  # Usa el decorador para requerir autenticacion
def protected_route():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return "Hola usuario autenticado!! B)"

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return {"message": "Logout exitoso"}, 200

@app.route('/')
@limiter.limit("3 per minute")
def home():
    return "Hello world!\nAqui tienes un limite de 3 peticiones por minuto :)"

@app.route('/pagina')
def pagina():
    return "Esta es la pagina en el endpoint /pagina.\nSin limite especifico pero es Afectado por el limite global de 10 por hora c:"

@app.route('/usuarios')
@limiter.limit("2 per minute")  # Limitar la consulta de usuarios a 2 por min
def usuarios():
    # Funcion para obtener la lista de usuarios de la base de datos
    try:
        # Establece la conexion con la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        # Consulta para obtener los usuarios
        query = sql.SQL("SELECT * FROM users")
        # Ejecuta la consulta
        cursor.execute(query)
        # Obtén todos los resultados
        users = cursor.fetchall()     
        # Cierra el cursor y la conexion
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return {"error": str(e)}

    return users

@app.route('/usuarios/torre')
@limiter.limit("3 per minute")  # Limitar la consulta específica de usuarios a 3 por hora
def usuariostorre():
    # Funcion para obtener la lista de usuarios de la base de datos
    try:
        # Establece la conexión con la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        # Consulta para obtener los usuarios
        query = sql.SQL("SELECT * FROM users WHERE device = 'desktop'")
        # Ejecuta la consulta
        cursor.execute(query)
        # Obtén todos los resultados
        users = cursor.fetchall()     
        # Cierra el cursor y la conexión
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return {"error": str(e)}

    return users

@app.route('/upload', methods=['POST'])
@login_required # protegemos esta ruta con inicio de sesion requerido
def upload_file():
    if 'file' not in request.files:
        return {"error": "No se envió ningún archivo"}, 400
    file = request.files['file']
    if file.filename == '':
        return {"error": "Nombre de archivo vacío"}, 400
    if file and allowed_file(file.filename):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        if os.path.exists(file_path):
            return {"error": "El archivo ya existe"}, 400
        try:
            file.save(file_path)
            return {"message": "Archivo cargado exitosamente"}, 201
        except Exception as e:
            return {"error": f"Error al guardar el archivo: {str(e)}"}, 500
    else:
        return {"error": "Tipo de archivo no permitido"}, 400

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    if allowed_file(filename):
        try:
            return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
        except FileNotFoundError:
            return {"error": "Archivo no encontrado"}, 404
    else:
        return {"error": "Tipo de archivo no permitido"}, 400

# Manejo de usuarios bloqueados por exceder el límite
@app.errorhandler(429)
def ratelimit_handler(e):
    return {"error": "Limite de peticiones excedido. Intentelo de nuevo más tarde.  " + str(e)}, 429

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
