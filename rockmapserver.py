import os
from dbmanager import DbManager
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename


IMAGEN = 'file'
NOMBRE = 'nombre'
ALTURA = 'altura'
ZONA = 'zona'
PARQUE = 'parque'
PUNTO1 = 'punto1'
PUNTO2 = 'punto2'
PUNTO3 = 'punto3'
PUNTO4 = 'punto4'
PAIS = 'pais'
ADDRESS = 'localhost'
port = 27017
DIFICULTAD = 'dificultad'

# Inicializar la app de Flask
app = Flask(__name__)

# Ubicacion de archivos de imagen
app.config['UPLOAD_FOLDER'] = 'uploads/'
# Extensiones permitidas
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# Determina si un archivo es aceptado por el servidor
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# Ruta que muestra una peticion AJAX para probar webservice
@app.route('/')
def index():
    return render_template('index.html')


# Ruta para subir una ruta con todos sus parametros
@app.route('/upload', methods=['POST'])
def upload():
    # Obtiene la imagen
    print 'Subiendo imagen...'
    file = request.files[IMAGEN]
    print request.files
    print request.form
    nombre = request.form.getlist('nombre')[0]

    pais = request.form.getlist(PAIS)[0]
    altura = request.form.getlist(ALTURA)[0]
    zona = request.form.getlist(ZONA)[0]
    parque = request.form.getlist(PARQUE)[0]
    p1 = request.form.getlist(PUNTO1)[0]
    p2 = request.form.getlist(PUNTO2)[0]
    p3 = request.form.getlist(PUNTO3)[0]
    p4 = request.form.getlist(PUNTO4)[0]
    dificultad = request.form.getlist(DIFICULTAD)[0]
    # Revisa si la imagen es valida
    if file and allowed_file(file.filename.lower()):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup 
        print 'Guardando imagen del cliente con nombre ' + file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        manager = DbManager(ADDRESS,port)
        manager.agregar_ruta(os.path.join(app.config['UPLOAD_FOLDER'], filename),nombre,altura,zona,parque,p1,p2,p3,p4,pais,dificultad)
        print 'Se guardo la ruta de nombre ' + nombre
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        return redirect(url_for('uploaded_file',
                                filename=filename))
    else:
    	return 'error'

@app.route('/rutas/<pais>')
def rutas(pais):
    manager = DbManager(ADDRESS,port)
    resultado = manager.rutas_por_pais(pais)
    return resultado

# Despliega la imagen
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/parques/<pais>')
def parques_pais(pais):
    manager = DbManager(ADDRESS,port)
    resultado = manager.parques_por_pais(pais)
    return resultado

@app.route('/nuevoparque', methods=['POST'])
def agregar_parque():
    nombre = request.form.getlist(NOMBRE)[0]
    pais = request.form.getlist(PAIS)[0]
    p1 = request.form.getlist(PUNTO1)[0]
    p2 = request.form.getlist(PUNTO2)[0]

    if nombre and pais and p1 and p2:
        manager = DbManager(ADDRESS,port)
        manager.agregar_parque(pais,nombre,p1,p2)
        print 'Se agrego el parque: ' + nombre + ' pais: ' + pais 
        return "Agregado"
    else:
        print 'Imposible agregar el parque: ' + nombre
        return "No se ha agregado"




# main del servidor
if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("8080"),
        debug=True
    )
