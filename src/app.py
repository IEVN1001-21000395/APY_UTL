from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from config import config

"""
GET, POST, PUT, DELETE
"""

app = Flask(__name__)

con = MySQL(app)

@app.route("/alumnos", methods=['GET'])
def lista_alumnos():
    try:
        cursor = con.connection.cursor()
        sql = "SELECT * FROM alumnos"
        cursor.execute(sql)
        datos = cursor.fetchall()
        alumnos = []
        for fila in datos:
            alumno = {"matricula": fila[0], "nombre": fila[1],
                    "apaterno": fila[2], "amaterno": fila[3],
                    "correo": fila[4]}
            alumnos.append(alumno)
        return jsonify({'alumnos': alumnos, 'mensaje': 'Lista de alumnos', 'exito': True})
    except Exception as ex:
        return jsonify({"message": "error {}".format(ex), 'exito': False}), 500

def leer_alumno_bd(matricula):
    try:
        cursor = con.connection.cursor()
        sql = "SELECT * FROM alumnos WHERE matricula = {0}".format(matricula)
        cursor.execute(sql)
        datos = cursor.fetchone()

        if datos is not None:
            alumno = {"matricula": datos[0], "nombre": datos[1],
                    "apaterno": datos[2], "amaterno": datos[3],
                    "correo": datos[4]}
            return alumno
        else:
            return None
    except Exception as ex:
        return jsonify({"message": "error {}".format(ex), 'exito': False}), 500

@app.route("/alumnos/<mat>", methods=['GET'])
def obtener_alumno(mat):
    try:
        alumno = leer_alumno_bd(mat)
        if alumno is not None:
            return jsonify({'alumno': alumno, 'mensaje': 'Alumno encontrado', 'exito': True})
        else:
            return jsonify({'alumno': None, 'mensaje': 'Alumno no encontrado', 'exito': False})
    except Exception as ex:
        return jsonify({"message": "error {}".format(ex), 'exito': False}), 500
    
@app.route("/alumnos", methods=['POST'])
def registrar_alumnos():
    try:
        alumno=leer_alumno_bd(request.json['matricula'])
        if alumno != None:
            return jsonify({'mensaje':"Alumno ya existe, no se puede duplicar",'exito':False})
        else:
            cursor=con.connection.cursor()
            sql="""Insert into alumnos(matricula,nombre,apaterno,amaterno,correo)
            values('{0}','{1}','{2}','{3}','{4}')""".format(request.json['matricula'],
                request.json['nombre'],request.json['apaterno'],request.json['amaterno'],request.json['correo'])
            cursor.execute(sql)
            con.connection.commit()
            return jsonify({'mensaje':"Alumno regristrado","exito":True})
    except Exception as ex:
        return jsonify({'mensaje':"Error",'exito':False})

def pagina_no_encontrada(error):
    return "<h1>Pagina no encontrada</h1>", 404

if __name__ == "_main_":
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(host='0.0.0.0', port=5000)