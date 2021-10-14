from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/login')
def login():
    return render_template ('index.html')

@app.route('/paginicio',methods=["POST"])   
def paginicio():
    nombre="estudiante"
    if ((request.form["name"]=="estudiante" and request.form["Pw"]=="estudiante1") or 
    (request.form["name"]=="profesor" and request.form["Pw"]=="profesor1")
     or(request.form["name"]=="superadmin" and request.form["Pw"]=="superadmin1")):

        return render_template ('paginicio.html')
    else:
        print("usuario no valido")
        return render_template ('index.html')

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

if __name__=='__main__':
    app.run(debug=True, port=80)

