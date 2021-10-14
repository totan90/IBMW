from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/login')
@app.route('/login/')
def index():
    return render_template('index.html')

@app.route('/home',methods=["GET","POST"])
def home():
    return render_template('contents/home.html')

@app.route('/usuarios',methods=["GET"])
def usuarios():
    return render_template('contents/usuarios.html')

@app.route('/productos',methods=["GET"])
def productos():
    return render_template('contents/producto.html')

@app.route('/proveedores',methods=["GET"])
def proveedores():
    return render_template('contents/proveedores.html')

@app.route('/usuarios/crear',methods=["POST"])
def crearUsuarios():
    return "crear usuario"

@app.route('/productos/crear',methods=["POST"])
def crearProductos():
    return "crear producto"

@app.route('/proveedores/crear',methods=["POST"])
def crearProveedores():
   return "crear proveedor"

@app.route('/usuarios/actualizar',methods=["PUT"])
def actualizarUsuarios():
    return "actualizar usuario"

@app.route('/productos/actualizar',methods=["PUT"])
def actualizarProductos():
    return "actualizar producto"

@app.route('/proveedores/actualizar',methods=["PUT"])
def actualizarProveedores():
   return "actualizar proveedor"

@app.route('/usuarios/eliminar',methods=["DELETE"])
def eliminarUsuarios():
    return "eliminar usuario"

@app.route('/productos/eliminar',methods=["DELETE"])
def eliminarProductos():
    return "eliminar producto"

@app.route('/proveedores/eliminar',methods=["DELETE"])
def eliminarProveedores():
   return "eliminar proveedor"

if __name__ == '__main__':
    app.run(port=8080, debug=True)