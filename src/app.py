from flask import Flask, request, jsonify
from flask_mysqldb import Mysql

from config import config 


app=Flask(__name__)

con=MySQL(app)

@app.route("/alumnos",methods=['GET'])
def lista_alumnos():
    try:
        cursor=con.connection.curso()
        sql="select * from alumnos"
        cursor.execute(sql)
        datos=cursor.fetchall()
        alumnos=[]
        for fila in datos:
            alumno={"matricula":fila[0],"nombre":fila[1],"apaterno":fila[2],"amaterno":fila[3],"correo":fila[4]}
            alumnos.append(alumno)
        return jsonify({'alumnos':alumnos,'mensaje':'Lista de alumnos','exito':True})
    except Exception as ex:
        return jsonify({"message":"error {}".format(ex),'exito':False})
    
    if __name__=="__main__":
        app.config.from_object(config['development'])
        app.register_error_hander(404,pagina_no_encontrada)
        app.run(host='0.0.0.0',port=500)

