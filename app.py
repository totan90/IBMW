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

@app.route('/productos')
def productos():
    return render_template('contents/productos.html')

@app.route('/proveedores')
def proveedores():
    return render_template('contents/proveedores.html')

if __name__ == '__main__':
    app.run(port=8080, debug=True)