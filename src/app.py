from flask import Flask ,jsonify ,request
# del modulo flask importar la clase Flask y los métodos jsonify,request
from flask_cors import CORS       # del modulo flask_cors importar CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app=Flask(__name__)  # crear el objeto app de la clase Flask
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend

# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:Oracle_4@localhost/proyecto'
# URI de la BBDD                          driver de la BD  user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow

# defino la tabla
class Usuario(db.Model):   # la clase Usuario hereda de db.Model    
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    nombre=db.Column(db.String(100))
    mail=db.Column(db.String(150))
    imagen=db.Column(db.String(400))
    def __init__(self,nombre,mail,imagen):   #crea el  constructor de la clase
        self.nombre=nombre   # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.mail=mail
        self.imagen=imagen


    #  si hay que crear mas tablas , se hace aqui


with app.app_context():
    db.create_all()  # aqui crea todas las tablas
#  ************************************************************
class UsuarioSchema(ma.Schema):
    class Meta:
        fields=('id','nombre','mail','imagen')


usuario_schema=UsuarioSchema()            # El objeto usuario_schema es para traer un usuario
usuarios_schema=UsuarioSchema(many=True)  # El objeto usuarios_schema es para traer multiples registros de usuario


# crea los endpoint o rutas (json)
@app.route('/usuarios',methods=['GET'])
def get_Usuarios():
    all_usuarios=Usuario.query.all()         # el metodo query.all() lo hereda de db.Model
    result=usuarios_schema.dump(all_usuarios)  # el metodo dump() lo hereda de ma.schema y
                                                 # trae todos los registros de la tabla
    return jsonify(result)                       # retorna un JSON de todos los registros de la tabla


@app.route('/usuarios/<id>',methods=['GET'])
def get_usuario(id):
    usuario=Usuario.query.get(id)
    return usuario_schema.jsonify(usuario)   # retorna el JSON de un usuario recibido como parametro


@app.route('/usuarios/<id>',methods=['DELETE'])
def delete_usuario(id):
    usuario=Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return usuario_schema.jsonify(usuario)   # me devuelve un json con el registro eliminado

@app.route('/usuarios', methods=['POST']) # crea ruta o endpoint
def create_usuario():
    #print(request.json)  # request.json contiene el json que envio el cliente
    nombre=request.json['nombre']
    mail=request.json['mail']
    imagen=request.json['imagen']
    new_usuario=Usuario(nombre,mail,imagen)
    db.session.add(new_usuario)
    db.session.commit()
    return usuario_schema.jsonify(new_usuario)

@app.route('/usuarios/<id>' ,methods=['PUT'])
def update_usuario(id):
    usuario=Usuario.query.get(id)
 
    usuario.nombre=request.json['nombre']
    usuario.mail=request.json['mail']
    usuario.imagen=request.json['imagen']

    db.session.commit()
    return usuario_schema.jsonify(usuario)
 

# programa principal *******************************
if __name__=='__main__':  
    app.run(debug=True, port=5000)    # ejecuta el servidor Flask en el puerto 5000
