from flask import Flask, render_template, request, jsonify, redirect, session, url_for
from flask.helpers import flash, url_for
from werkzeug.wrappers import response
from formularios import FormPart, Login
from markupsafe import escape
from db import consult_action, consult_select
from werkzeug.security import check_password_hash, generate_password_hash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

#ruta para abrir formulario de login
@app.route('/')
@app.route('/login')
@app.route('/login/')
def index():
    frm = Login()
    return render_template('index.html',form=frm)

#ruta para salir del dashboard
@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('index'))

#ruta para comprobar el usuario y entrar al dashboard
@app.route('/home',methods=["GET","POST"])
def home():
    #recuperacion de datos
    if request.method == "POST" :
        user = escape(request.form['username'].strip()).lower()
        pwd = escape(request.form['password'].strip())
        #preparamos para consultar si el usuario existe
        sql = f"SELECT * FROM usuarios WHERE userName = '{user}'"
        #realizamos la consulta
        res = consult_select(sql)
        #si el usuario existe traemos los datos para crear la sesion
        if len(res)!=0:
            sql2 = f"SELECT password, nombresUsuario, userName, idROl FROM usuarios WHERE userName = '{user}'"
            res2 = consult_select(sql2)
            passw = res2[0][0]
            confirmPassword = check_password_hash(passw,pwd)
            if confirmPassword == True :
                #si el usuario y la password son correctos creamos la session y lo enviamos al dashboard
                session['name'] = res2[0][1]
                session['userName'] = res2[0][2]
                session['rol'] = res2[0][3]
                sql = "SELECT * FROM productos INNER JOIN img ON productos.idImg = img.id WHERE cantidadDisponibleProducto < cantidadMinimaProducto"
                res = consult_select(sql)
                sql2 = "SELECT NombreProducto,cantidadMinimaProducto,cantidadDisponibleProducto,(cantidadDisponibleProducto-cantidadMinimaProducto) AS total FROM productos INNER JOIN img ON productos.idImg = img.id WHERE cantidadDisponibleProducto > cantidadMinimaProducto AND total < 9"
                res2 = consult_select(sql2)
                print(res2)
                return render_template('contents/home.html',datos=res,datos2=res2)
            else :
                #si el usuario no existe lo redirigimos al login
                flash('Usuario o Contraseña incorrectos')
                return redirect('/')
        else :
            #si el usuario no existe lo redirigimos al login
            flash('Usuario o Contraseña incorrectos')
            return redirect('/')
    else :
        if 'userName' and 'name' in session :
            sql = "SELECT * FROM productos INNER JOIN img ON productos.idImg = img.id WHERE cantidadDisponibleProducto < cantidadMinimaProducto"
            res = consult_select(sql)
            sql2 = "SELECT nombreProducto,cantidadMinimaProducto,cantidadDisponibleProducto FROM productos INNER JOIN img ON productos.idImg = img.id"
            res2 = consult_select(sql2)
            return render_template('contents/home.html',datos=res)
        else :
            return redirect(url_for('index'))
        # print(res2)
        # array = []
        # cdp = res2[0][2]
        # cmp = res2[0][1]
        # producto = res2[0][0]
        # i = 0
        # while len(res2) > i :
        #     if float(cdp) - float(cmp) == 2 :
        #         array.append(producto)
        #         print(array)
        #         i = i+1
        # if len(res)!=0 :

# routas de usuarios
@app.route('/productos/alerta',methods=["GET"])
def productosAlert():
    sql =  "SELECT * FROM productos INNER JOIN roles ON productos.idImg = img.id WHERE cantidadDisponibleProducto < cantidadMinimaProducto"
    res = consult_select(sql)
    if len(res)!=0 :
        frm = FormPart()
        return jsonify({'data':res})
        # return render_template('contents/usuarios.html',form=frm, data=res)


@app.route('/usuarios',methods=["GET"])
def usuarios():
    if 'userName' and 'name' in session :
        sql =  "SELECT * FROM usuarios INNER JOIN roles ON usuarios.idRol = roles.id"
        res = consult_select(sql)
        if len(res)!=0 :
            frm = FormPart()
            return render_template('contents/usuarios.html',form=frm, data=res)
    else :
        return redirect(url_for('index'))

@app.route('/form/crear',methods=["GET"])
def formUser():
    if 'userName' and 'name' in session :
        frm = FormPart()
        return render_template('contents/formUser.html',form=frm)
    else :
        return redirect(url_for('index'))

@app.route('/usuarios/crear',methods=["POST"])
def crearUsuarios():
    if 'userName' and 'name' in session :
        #recuperacion de datos
        nombresUsuario = escape(request.form['nombres'].strip()).lower()
        apellidosUsuario = escape(request.form['apellidos'].strip()).lower()
        tipo_documento = escape(request.form['tipo_documento'].strip()).lower()
        numero_documento = escape(request.form['numero_documento'].strip())
        emailUsuario = escape(request.form['email'].strip())
        celularUsuario = escape(request.form['celular'].strip())
        direccionUsuario = escape(request.form['direccion'].strip())
        username = escape(request.form['username'].strip()).lower()
        password = generate_password_hash(escape(request.form['password'].strip()))
        idROl = escape(request.form['roles'])
        activo = 'si'
        #preparacion de sql
        sql = "INSERT INTO usuarios(nombresUsuario, apellidosUsuario,tipoDocumento,numeroDocumento,emailUsuario,celularUsuario,direccionUsuario,username,password,idRol,activo) VALUES (?,?,?,?,?,?,?,?,?,?,?) "
        #insertando los datos
        res = consult_action(sql,(nombresUsuario,apellidosUsuario,tipo_documento, numero_documento,emailUsuario,celularUsuario,direccionUsuario,username,password,idROl,activo))
        if res!=0 :
            flash('Usuario registrado con éxito ')
            return redirect(url_for('usuarios'))
    else :
        return redirect(url_for('index'))


@app.route('/usuarios/view/<string:id>',methods=["POST","GET"])
def buscarUser(id):
    if 'userName' and 'name' in session :
        sql = f"SELECT * FROM usuarios INNER JOIN roles ON usuarios.idRol = roles.id  WHERE usuarios.id = '{id}'"
        res = consult_select(sql)
        return render_template('contents/viewUser.html',datos=res);
    else :
        return redirect(url_for('index'))

@app.route('/usuarios/edit/<string:id>',methods=["GET"])
def userEdit(id):
    if 'userName' and 'name' in session :
        sql = f"SELECT * FROM usuarios INNER JOIN roles ON usuarios.idRol = roles.id  WHERE usuarios.id = '{id}'"
        res = consult_select(sql)
        frm = FormPart()
        return render_template('contents/editUser.html',form=frm,datos=res)
    else :
        return redirect(url_for('index'))

@app.route('/usuarios/actualizar/<string:id>',methods=["PUT","POST"])
def actualizarUsuarios(id):
    if 'userName' and 'name' in session :
        #recuperamos los datos
        nombresUsuario = escape(request.form['nombres'].strip()).lower()
        apellidosUsuario = escape(request.form['apellidos'].strip()).lower()
        tipo_documento = escape(request.form['tipo_documento'].strip()).lower()
        numero_documento = escape(request.form['numero_documento'].strip())
        emailUsuario = escape(request.form['email'].strip())
        celularUsuario = escape(request.form['celular'].strip())
        direccionUsuario = escape(request.form['direccion'].strip())
        username = escape(request.form['username'].strip()).lower()
        idROl = escape(request.form['roles'])
        activo = 'si'
        password = escape(request.form['password'].strip())
        #observamos cambios en la password
        if(password):
            passwordCfd = generate_password_hash(escape(request.form['password'].strip()))
            sql = f"UPDATE usuarios SET nombresUsuario = ?, apellidosUsuario = ?,tipoDocumento = ?,numeroDocumento = ?,emailUsuario = ?,celularUsuario = ?,direccionUsuario = ?,username = ?,password = ?,idRol = ?,activo =? WHERE id = {id} "
            res = consult_action(sql,(nombresUsuario,apellidosUsuario,tipo_documento, numero_documento,emailUsuario,celularUsuario,direccionUsuario,username,passwordCfd,idROl,activo))
            return redirect(url_for('usuarios'))
            
        else :
            sql = f"UPDATE usuarios SET nombresUsuario = ?, apellidosUsuario = ?,tipoDocumento = ?,numeroDocumento = ?,emailUsuario = ?,celularUsuario = ?,direccionUsuario = ?,username = ?,idRol = ?,activo =? WHERE id = {id} "
            res = consult_action(sql,(nombresUsuario,apellidosUsuario,tipo_documento, numero_documento,emailUsuario,celularUsuario,direccionUsuario,username,idROl,activo))
            return redirect(url_for('usuarios'))
    else :
        return redirect(url_for('index'))
 
@app.route('/form/delete/<string:id>',methods=["GET"])
def deleteUser(id):
    if 'userName' and 'name' in session :
        sql =  f"SELECT * FROM usuarios WHERE id = {id}"
        res = consult_select(sql)
        frm = FormPart()
        return render_template('contents/deleteUser.html',form=frm,datos=res)
    else :
        return redirect(url_for('index'))

@app.route('/usuarios/delete/<string:id>',methods=["GET","POST","PUT"])
def deleteUsuarios(id):
    if 'userName' and 'name' in session :
        sql =  f"SELECT nombresUsuario, activo FROM usuarios WHERE id = {id}"
        res = consult_select(sql)
        name = res[0][0]
        if res[0][1] == 'si' :
            activo = 'no'
        else :
            activo = 'si'

        sql = f"UPDATE usuarios SET nombresUsuario =?, activo =? WHERE id = {id} "
        res = consult_action(sql,(name,activo))
        return redirect(url_for('usuarios'))
    else :
        return redirect(url_for('index'))

@app.route('/usuarios/search/',methods=["GET","POST"])
def searchUsuarios():
    if 'userName' and 'name' in session :
        atributo = escape(request.form['atributo'])
        valor = escape(request.form['valor']).lower()
        sql =  f'SELECT * FROM usuarios INNER JOIN roles ON usuarios.idRol = roles.id WHERE {atributo} LIKE "%{valor}%"'
        res = consult_select(sql)
        return render_template('contents/usuarios.html', data=res)
    else :
        return redirect(url_for('index'))

@app.route('/username/',methods=["POST"])
def username():
    username = request.form['username'].lower()
    sql = f"SELECT * FROM usuarios WHERE userName = '{username}'"
    res = consult_select(sql)
    if len(res)==0 :
        response = 'username free'
        return response;
    else :
        response = 'username busy'
        return response;




@app.route('/productos',methods=["GET"])
def productos():
    return render_template('contents/producto.html')

@app.route('/proveedores',methods=["GET"])
def proveedores():
    return render_template('contents/proveedores.html')


@app.route('/productos/crear',methods=["POST"])
def crearProductos():
    return "crear producto"

@app.route('/proveedores/crear',methods=["POST"])
def crearProveedores():
   return "crear proveedor"



@app.route('/productos/actualizar',methods=["PUT"])
def actualizarProductos():
    return "actualizar producto"

@app.route('/proveedores/actualizar',methods=["PUT"])
def actualizarProveedores():
   return "actualizar proveedor"



@app.route('/productos/eliminar',methods=["DELETE"])
def eliminarProductos():
    return "eliminar producto"

@app.route('/proveedores/eliminar',methods=["DELETE"])
def eliminarProveedores():
   return "eliminar proveedor"





if __name__ == '__main__':
    app.run(port=8080, debug=True)