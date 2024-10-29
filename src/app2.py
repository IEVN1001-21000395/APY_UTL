from flask import Flask, render_template
app=Flask(__name__)

@app.route("/")
def index():
    titulo='IEVN-1001'
    list=['Pedro,Pablo,Juan,Fulta']
    return render_template('uno.html',titulo=titulo,list=list)


@app.route("/user/<string:user>") #rutas 
def user(user):
    return "El usuario es: {}".format(user)

@app.route("/numero/<int:n1>") #rutas 
def numero(n1):
    return "El numero es: {}".format(n1)

@app.route("/user/<string:nom>/int:id") #rutas 
def datos(nom,id):
    return "El numero es: {}".format(id,nom)

@app.route("/suma/<float:n1>/float:n2") #rutas 
def suma(n1,n2):
    return "La suma es : {}".format(n2+n1)

@app.route("/default")
@app.route("/default/<string:nom>") #rutas 
def nom2(nom='Santiago'):
    return "<h1> El nombre es : {}</h1>".format(nom)#definimos 

if __name__=="__main__":
    app.run(debug=True)