"""
Trabajar con la base de datos.

   Consultas de acción ::   Modifican la base de datos y reportan la 
                            cantidad de filas que fueron afectadas (int)

   Consultas de selección   Recuperan información de la base de datos 
                            y retornan los registros  (list - RecordSet, ResultSet)
"""

import sqlite3
from sqlite3 import Error

URL_DB = 'NotasVF.db'

def seleccion(sql) -> list:
    """ Ejecuta una consulta de selección sobre la base de datos """
    try:
        with sqlite3.connect(URL_DB) as con:        # Conectarse a la base de datos con manejador de contextos(Cierra la BD cuando se deje de utilizar)
            cur = con.cursor()                      # Crea un área intermedia para gestión de los contenidos
            res = cur.execute(sql).fetchall()       # Se obtienen los registros devueltos
    except:
        res = None
    return res

def accion(sql, datos) -> int:
    """ Ejecuta una consulta de acción sobre la base de datos """
    try:
        with sqlite3.connect(URL_DB) as con:
            cur = con.cursor()
            res = cur.execute(sql,datos).rowcount   # Ejecutar la consulta
            if res!=0:                              # Verificar si se realizó algún cambio
                con.commit()                        # Volver permanente el cambio
    except:
        res = 0
    return res

def base_conexion():
    try:
        conectar=sqlite3.Connection('NotasVF.db')
        return conectar
    except  Error:
        print(Error)