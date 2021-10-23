from flask import Flask, render_template, request, redirect, flash, session, redirect
from markupsafe import escape
import os
import dB
from dB import accion, seleccion

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
@app.route('/home/')
@app.route('/index/')
def inicio():
    return render_template('index.html')

@app.route('/registroGrup/',methods=['GET','POST'])
def registro_grupos():
    if request.method == 'GET':
        return render_template('FormularioGrupos.html')
    else:
            grupoid=request.form['iddegrupo']
            Nombregrup=request.form['nombre']
            semestre=request.form['semestre']
            jornada=request.form['Jornada']

            conexion=dB.base_conexion()
            strsql="insert into Grupos (GrupoID, Nombre, Semestre,Jornada) values('{}','{}','{}','{}')" .format(grupoid,Nombregrup,semestre,jornada)
            cursosObj=conexion.cursor()
            cursosObj.execute(strsql)
            conexion.commit()
            conexion.close()

            flash("Registro Exitoso")
            return render_template ('paginicio.html')

@app.route('/registroMat/',methods=['GET','POST'])
def registro_materias():
    if request.method == 'GET':
        return render_template('FormularioMaterias.html')
    else:
            materiaid=request.form['iddemateria']
            Nombremat=request.form['nombremat']
            IDgrupo=request.form['IDgrupo']
            IDprofesor=request.form['IDdocente']

            conexion=dB.base_conexion()
            strsql="insert into Materias (MateriaID, Nombre, Grupoid,Profesorid) values('{}','{}','{}','{}')" .format(materiaid,Nombremat,IDgrupo,IDprofesor)
            cursosObj=conexion.cursor()
            cursosObj.execute(strsql)
            conexion.commit()
            conexion.close()

            flash("Registro Exitoso")
            return render_template ('paginicio.html')


@app.route('/index/', methods=["POST"])
def login():
    # recuperar los datos del formulario
    usr = escape(request.form["name"].strip()) # Dificultar la inyección de código y quitar espacios en blanco al comienzo o al final
    cla = escape(request.form["Pw"].strip()) 
    
    # Preparar la consulta
    if (request.form['selectrol']=="2"):
        sql = f'SELECT Nombres, Contraseña FROM Estudiantes WHERE DNI="{usr}"'
    elif (request.form['selectrol']=="1"):
        sql = f'SELECT Nombres, Contraseña FROM Profesores WHERE ID="{usr}"'    

    # Ejecutar la consulta
    res = seleccion(sql)
    # Proceso la respuesta
    if len(res)==0:
        flash('ERROR: Usuario no existe')
        return render_template('index.html')
    else:
        # Recupero el valor de la clave
        clave = str(res[0][1])
        
        if clave == cla:
            session.clear()
            session['nom'] = res[0][0]
            return redirect('/paginicio/')
        else:
            flash('ERROR: Clave invalida')
            return render_template('index.html')

@app.route('/registro/',methods=['GET','POST'])
def registro_datos():
    if request.method == 'GET':
        return render_template('FormularioPrimerIngreso.html')
    else:
        if (request.form['selectrol']=="2"):
            dNI=request.form['Documento']
            Nom=request.form['nombre']
            Ape=request.form['apellido']
            Nombres= Nom + " " + Ape
            Genero=request.form['genero']
            Contraseña=request.form['contrasena']
            Nacido=request.form['fecha de nacimiento']
            
            conexion=dB.base_conexion()
            strsql="insert into Estudiantes (DNI, Nombres, Genero,Contraseña,Nacido) values('{}','{}','{}','{}', '{}')" .format(dNI,Nombres,Genero,Contraseña,Nacido)
            cursosObj=conexion.cursor()
            cursosObj.execute(strsql)
            conexion.commit()
            conexion.close()
                        
        elif (request.form['selectrol']=="1"):
            Id=request.form['Documento']
            Nom=request.form['nombre']
            Ape=request.form['apellido']
            Nombres= Nom + " " + Ape
            Genero=request.form['genero']
            Estado=request.form['Documento']
            Contraseña=request.form['contrasena']
            prueba = request.form['selectrol']
            print(prueba)
            if prueba == "1":
                print(True)

            conexion=dB.base_conexion()
            strsql="insert into Profesores (ID, Nombres, Genero,Contraseña) values('{}','{}','{}','{}')" .format(Id,Nombres,Genero,Contraseña)
            cursosObj=conexion.cursor()
            cursosObj.execute(strsql)            
            conexion.commit()
            conexion.close()
        
        flash("Registro Exitoso")
        return render_template ('index.html')

@app.route('/paginicio/')   
def paginicio():
    if "nom" in session:
        perfnom = session['nom']
        return render_template ('paginicio.html', nombres= perfnom)
    else:
        flash("Inicie sesión para utilizar plataforma")
        return render_template ('index.html')

@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/')

@app.route('/recuperar contrasena')
def recuperar_contrasena():
    return render_template ('Olvido su contraseña.html')

@app.route('/ResumenNotas')
def ResumenNotas():
    return render_template ('redumenNotas.html')

@app.route('/perfil')
def perfil():
    return render_template ('infoPersonal.html')

@app.route('/actividades')
def actividades():
    return render_template ('actyretro.html') 

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



