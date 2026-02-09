from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)

def conectarCampus():
    conexion = psycopg2.connect(
        host="localhost",
        port="5432",
        database="campus",
        user="postgres",
        password="admin"
    )
    return conexion

@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        usuario = request.form["user"]
        password = request.form["password"]
        print(password)
        

        
        try:
            conn = conectarCampus()
            cursor = conn.cursor()
            # Obtener el hash de la contraseña y el email para el usuario
            cursor.execute("SELECT password, usuario_email FROM usuarios WHERE usuario = %s", (usuario,))
            resultado = cursor.fetchone()
            cursor.close()
            conn.close()

            if resultado:
                stored_hash, email = resultado[0], resultado[1]
                # Verificar el password con el hash almacenado
                if check_password_hash(stored_hash, password):
                    return render_template("user.html", usuario=usuario, email=email)
                else:
                    return redirect(url_for("registro"))
            else:
                return redirect(url_for("registro"))
        except Exception as e:
            print(f"Error: {e}")
            return redirect(url_for("registro"))
    
    return render_template("login.html")

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        usuario = request.form["user"]
        password = request.form["password"]
        email = request.form["email"]
        
        password_hash = generate_password_hash(password)

        try:
            conn = conectarCampus()
            cursor = conn.cursor()
            # Comprobar si el email ya está registrado
            cursor.execute("SELECT 1 FROM usuarios WHERE usuario_email = %s", (email,))
            existe = cursor.fetchone()
            if existe:
                cursor.close()
                conn.close()
                return render_template("registro.html", error="El email ya está registrado")

            # Insertar nuevo usuario
            cursor.execute("INSERT INTO usuarios (usuario, password, usuario_email) VALUES (%s, %s, %s)", (usuario, password_hash, email))
            conn.commit()
            cursor.close()
            conn.close()

            # Después del registro, mostrar página de usuario
            return render_template("login.html")
        except Exception as e:
            print(f"Error al registrar: {e}")
            return render_template("registro.html", error="Error al registrar el usuario")
    
    return render_template("registro.html")

# @app.route("/login", methods=["GET", "POST"])
# def login():
#     # Ruta alternativa para login (puede usarse además de /)
#     if request.method == "POST":
#         usuario = request.form["user"]
#         password = request.form["password"]
        
#         try:
#             conn = conectarCampus()
#             cursor = conn.cursor()
#             cursor.execute("SELECT password, usuario_email FROM usuarios WHERE usuario = %s", (usuario,))
#             resultado = cursor.fetchone()
#             cursor.close()
#             conn.close()

#             if resultado:
#                 stored_hash, email = resultado[0], resultado[1]
#                 if check_password_hash(stored_hash, password):
#                     return render_template("user.html", usuario=usuario, email=email)
#                 else:
#                     return redirect(url_for("registro"))
#             else:
#                 return redirect(url_for("registro"))
#         except Exception as e:
#             print(f"Error: {e}")
#             return redirect(url_for("registro"))
    
#     return render_template("login.html")

