from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        usuario = request.form["user"]
        password = request.form["password"]
        email = request.form["email"]
        color = request.form["color"]

        """Genera una nueva pagina (template) HTML que muestra el 
        usuario ingresado, su email y su color favorito.
        El return condicional actual no servira para nada en este caso."""

        print("Usuario ingresado:", usuario)
        print("Password ingresado:", password)
        return render_template("user.html", usuario=usuario, email=email, color=color)
        #return f"<p>Usuario {usuario} ha intentado iniciar sesión.<br><p>Tu correo es: {email}</p><br><p>Tu color favorito es: {color}</p>"

    return render_template("login.html")

