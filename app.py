from flask import Flask, render_template, request, redirect, url_for
import psycopg2

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
        
        try:
            conn = conectarCampus()
            cursor = conn.cursor()
            cursor.execute("SELECT usuario_email FROM usuarios WHERE usuario = %s AND password = %s", (usuario, password))
            resultado = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if resultado:
                # Login correcto
                email = resultado[0]
                return render_template("user.html", usuario=usuario, email=email)
            else:
                # Login incorrecto, redirigir a registro
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
            cursor.execute("INSERT INTO usuarios (usuario, password, usuario_email) VALUES (%s, %s, %s)", (usuario, password, email))
            conn.commit()
            cursor.close()
            conn.close()

            # Después del registro, mostrar página de usuario
            return render_template("login.html")
        except Exception as e:
            print(f"Error al registrar: {e}")
            return render_template("registro.html", error="Error al registrar el usuario")
    
    return render_template("registro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    # Ruta alternativa para login (puede usarse además de /)
    if request.method == "POST":
        usuario = request.form["user"]
        password = request.form["password"]
        
        try:
            conn = conectarCampus()
            cursor = conn.cursor()
            cursor.execute("SELECT usuario_email FROM usuarios WHERE usuario = %s AND password = %s", (usuario, password))
            resultado = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if resultado:
                email = resultado[0]
                return render_template("user.html", usuario=usuario, email=email)
            else:
                return redirect(url_for("registro"))
        except Exception as e:
            print(f"Error: {e}")
            return redirect(url_for("registro"))
    
    return render_template("login.html")

