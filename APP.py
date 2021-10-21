from flask import Flask, render_template, request, redirect, flash, redirect
from markupsafe import escape
import os
from dB import accion, seleccion

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
@app.route('/home/')
@app.route('/index/')
def inicio():
    return render_template('index.html')

@app.route('/index/', methods=["POST"])
def login():
    # recuperar los datos del formulario
    usr = escape(request.form["name"].strip()) # Dificultar la inyección de código y quitar espacios en blanco al comienzo o al final
    cla = escape(request.form["Pw"].strip()) 
    # Preparar la consulta
    sql = f'SELECT Contraseña FROM Estudiantes WHERE correo="{usr}"'
    # Ejecutar la consulta
    res = seleccion(sql)
    print(res)
    # Proceso la respuesta
    if len(res)==0:
        flash('ERROR: Usuario no existe')
        return render_template('index.html')
    else:
        # Recupero el valor de la clave
        clave = res[0][0]
        print(clave)
        if clave == cla:
            return redirect('/paginicio/')
        else:
            flash('ERROR: Clave invalida')
            return render_template('index.html')

@app.route('/paginicio/',methods=["GET", "POST"])   
def paginicio():
    return render_template ('paginicio.html')
    

@app.route('/registro',methods=['POST'])
def registro():
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
    return render_template ('actyretro.html') #cambiar cuando Mock de actividades este on-line

@app.route('/notasprof')
def notasprof():
    return render_template ('notasprofe.html')    

@app.route('/adminestu')
def adminestu():
    return render_template ('adminestu.html')    

@app.route('/formularioCambio')
def formularioCambio():
    return render_template ('formularioCambio.html')
    
@app.route('/infdeestudi')
def infdeestudi():
    return render_template ('infdeestudi.html')

if __name__ == '__main__':
    app.run(port=8080,debug=True)



