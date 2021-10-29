from flask import Flask, render_template, request, redirect, flash, session
from markupsafe import escape
import os
import dB
from dB import accion, seleccion
from hashlib import sha256
from werkzeug.security import generate_password_hash,check_password_hash    


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
        if "nom" in session and session['tipoU'] == "1":
            perfnom = session['nom']
                      
            sql = f'SELECT * FROM Grupos'
            
            resGrupo = seleccion(sql)
            return render_template ('AdminGrupos.html', grupos=resGrupo, nombres= perfnom, data=[('/registroMat/', 'Materias'), ('/ResumenNotas/', 'Notas')])
        else:
            flash("Inicie sesión para utilizar plataforma")
            return render_template ('index.html')
        
    else:
            grupoid=request.form['iddegrupo']
            Nombregrup=request.form['nombre']
            jornada=request.form['Jornada']

            conexion=dB.base_conexion()
            strsql="insert into Grupos (GrupoID, GNombre, Jornada) values('{}','{}','{}')" .format(grupoid,Nombregrup,jornada)
            cursosObj=conexion.cursor()
            cursosObj.execute(strsql)
            conexion.commit()
            conexion.close()

            flash("Grupo Almacenado")
            return redirect ('/registroGrup/')

@app.route('/registroGrup/delete/<idg>/')
def registro_grupos_edit(idg):
    conexion=dB.base_conexion()
    strsql = f'UPDATE Grupos SET GEstado=? WHERE GrupoID="{idg}"'
    cursosObj=conexion.cursor()
    cursosObj.execute(strsql,'D')
    conexion.commit()
    conexion.close()
    flash("Grupo Desactivado")
    return redirect ('/registroGrup/')


@app.route('/registroMat/',methods=['GET','POST'])
def registro_materias():    
    if request.method == 'GET':
        if "nom" in session and session['tipoU'] == "1":
            perfnom = session['nom']
                      
            sql = f'SELECT * FROM Materias'
            
            resMat = seleccion(sql)
            print(resMat)
            return render_template ('AdminMaterias.html', materias=resMat, nombres= perfnom, data=[('/registroGrup/', 'Grupos'), ('/ResumenNotas/', 'Notas')])
        else:
            flash("Inicie sesión para utilizar plataforma")
            return render_template ('index.html')
        
    else:
            materiaid=request.form['iddemateria']
            Nombremat=request.form['nombremat']
            semestre=request.form['semestre']
            
            conexion=dB.base_conexion()
            strsql="insert into Materias (CodMateria, Nombre, Semestre) values('{}','{}','{}')" .format(materiaid,Nombremat,semestre)
            cursosObj=conexion.cursor()
            cursosObj.execute(strsql)
            conexion.commit()
            conexion.close()

            flash("Registro Exitoso")
            return redirect ('/registroMat/')



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
    elif (request.form['selectrol']=="3"):
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
        if check_password_hash(clave,cla):
            session.clear()
            session['nom'] = res[0][0]
            session['usuario'] = usr
            session['tipoU'] = request.form['selectrol']
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
            Contraseña=generate_password_hash(request.form['contrasena'])
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
            Contraseña=generate_password_hash(request.form['contrasena'])
            prueba = request.form['selectrol']
            
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
    if "nom" in session and session['tipoU'] == "1":
        perfnom = session['nom']
        return render_template ('paginicio.html', nombres= perfnom, data=[('/registroMat/', 'Materias'), ('/ResumenNotas/', 'Notas'), ('/registroGrup/', 'Grupos')])
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

@app.route('/ResumenNotas/')
def ResumenNotas():
    return render_template ('redumenNotas.html')

@app.route('/perfil')
def perfil():
    return render_template ('infoPersonal.html')

@app.route('/actividades/', methods=['GET','POST'])
def actividades():

    if request.method == 'GET':
        if "nom" in session:
            perfnom = session['nom']
            perfusuario = str(session['usuario'])
                
            sql = f'SELECT Materias.GrupoId, Grupos.Nombre FROM Materias INNER JOIN Grupos ON Materias.GrupoId = Grupos.GrupoID WHERE Profesorid="{perfusuario}"'
            resMaterias = seleccion(sql)
                        
            # Proceso la respuesta
            if len(resMaterias)==0:
                flash('No tiene grupos asignados')
                return render_template ('actividades.html')
            else:
                return render_template ('actividades.html', materias = resMaterias, nombres= perfnom)

        else:
            flash("Inicie sesión para utilizar plataforma")
            return render_template ('index.html')

    else:
        # recuperar los datos del formulario    
        actgru = escape(request.form["grupoactvidades"].strip())
        actdes = escape(request.form["descripcion"].strip())
        actporc = escape(request.form["porcentaje"].strip())
        actfentre = request.form['fecentrega']

        
        conexion=dB.base_conexion()
        cursosObj=conexion.cursor()
        strsql="insert into Actividades(Descripcion, Porcentaje, Fecha_Entrega) values('{}', '{}', '{}')".format(actdes, actporc, actfentre)
        print(strsql)
        cursosObj.execute(strsql)            
        conexion.commit()
        conexion.close()

        flash("Registro Exitoso")
        return redirect('/actividades/')

    
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



