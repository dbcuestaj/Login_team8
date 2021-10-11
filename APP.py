from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def login():
    return render_template ('index.html')

@app.route('/paginicio')
def paginicio():
    return render_template ('paginicio.html')

@app.route('/registro',methods=['POST'])
def registro():
    print(request.form)
    return render_template ('paginicio.html')

@app.route('/recuperar contrasena')
def recuperar_contrasena():
    return render_template ('Olvido su contraseña.html')

@app.route('/crearUsuario')
def crear_usuario():
    return render_template ('FormularioPrimerIngreso.html')
@app.route('/ResumenNotas')
def ResumenNotas():
    return render_template ('redumenNotas.html')

@app.route('/perfil')
def perfil():
    return render_template ('infoPersonal.html')

@app.route('/actividades')
def actividades():
    return render_template ('pantilla.html')