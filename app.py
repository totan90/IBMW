from flask import Flask, render_template, request, jsonify, redirect, session, url_for
from flask.helpers import flash, url_for
from werkzeug.utils import secure_filename
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
                if res!= None and res2!= None:
                    return render_template('contents/home.html',datos=res,datos2=res2)
                else :
                    if res == None:
                        messageRes = "No existen productos por debajo del mínimo "
                    if res2 == None:
                        messageRes2 = "No existen productos cerca del mínimo "
                    return render_template('contents/home.html',messageRes=messageRes,messageRes2=messageRes2)
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
            if res!= None and res2!= None:
                return render_template('contents/home.html',datos=res,datos2=res2)
            else :
                if res == None:
                    messageRes = "No existen productos por debajo del mínimo "
                if res2 == None:
                    messageRes2 = "No existen productos cerca del mínimo "
                return render_template('contents/home.html',messageRes=messageRes,messageRes2=messageRes2)
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
        if len(res)!= 0 :
            return render_template('contents/usuarios.html', data=res)
        else : 
            return render_template('contents/usuarios.html', message='Sin resultados ')
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


#Todas la URLS de proveedores


@app.route('/proveedores',methods=["GET"])
def proveedores():
    if 'userName' and 'name' in session :
        sql =  "SELECT * FROM proveedores INNER JOIN img ON proveedores.id = img.idProveedores"
        res = consult_select(sql)
        if len(res)!=0 :
            frm = FormPart()
            return render_template('contents/proveedores.html',form=frm, data=res)
    else :
        return redirect(url_for('index'))

@app.route('/form/crear/proveedor/',methods=["GET"])
def formProveedor():
    if 'userName' and 'name' in session :
        frm = FormPart()
        return render_template('contents/formProveedor.html',form=frm)
    else :
        return redirect(url_for('index'))

@app.route('/proveedores/crear',methods=["POST"])
def crearProveedores():
    if 'userName' and 'name' in session :
        frm = FormPart()
        #recuperacion de datos proveedor
        nombresProveedor = escape(request.form['nombresProveedor'].strip()).lower()
        tipo_documento = escape(request.form['tipo_documento'].strip()).lower()
        numero_documento = escape(request.form['numero_documento'].strip())
        emailProveedor = escape(request.form['email'].strip())
        celularProveedor = escape(request.form['celular'].strip())
        direccionProveedor = escape(request.form['direccion'].strip())
        activo = 'si'
        logoProveedor = frm.logo.data
        nameImg = secure_filename(logoProveedor.filename)
        jinjaStart = "img/uploads/"
        urlImg = jinjaStart+nameImg
        logoSave = f"static/img/uploads/{nameImg}"
        logoProveedor.save(logoSave)

        if nombresProveedor and tipo_documento and numero_documento and emailProveedor and celularProveedor and direccionProveedor :
            #preparacion de sql
            sql = "INSERT INTO proveedores(nombresProveedor,tipoDocumento,numeroDocumento,celularProveedor,emailProveedor,direccionProveedor,activo) VALUES (?,?,?,?,?,?,?) "
            #insertando los datos
            res = consult_action(sql,(nombresProveedor,tipo_documento, numero_documento,celularProveedor,emailProveedor,direccionProveedor,activo))
            sql2 = "SELECT id FROM proveedores ORDER BY id DESC LIMIT 1"
            res2 = consult_select(sql2)
            proveedor_id = res2[0][0]
            producto_id = 0
            sql3 = "INSERT INTO img(nombreImg,idProducto,idProveedores) VALUES (?,?,?) "
            res3 = consult_action(sql3,(urlImg,producto_id, proveedor_id))

            if res!=0 and res2 != None and res3!=0:
                flash('Proveedor registrado con éxito ')
            else : 
                flash('Proveedor no registrado con éxito ')
            return redirect(url_for('proveedores'))
        else :
            flash('Fallo el registro faltaron campos por diligenciar')
            return redirect(url_for('formProveedor'))
    else :
        return redirect(url_for('index'))

@app.route('/proveedores/view/<string:id>',methods=["POST","GET"])
def buscarProveedor(id):
    if 'userName' and 'name' in session :
        sql =  f"SELECT * FROM proveedores INNER JOIN img ON proveedores.id = img.idProveedores WHERE proveedores.id = '{id}'"
        res = consult_select(sql)
        return render_template('contents/viewProveedores.html',datos=res);
    else :
        return redirect(url_for('index'))

@app.route('/proveedores/edit/<string:id>',methods=["GET"])
def proveedorEdit(id):
    if 'userName' and 'name' in session :
        sql =  f"SELECT * FROM proveedores INNER JOIN img ON proveedores.id = img.idProveedores WHERE proveedores.id = '{id}'"
        res = consult_select(sql)
        frm = FormPart()
        return render_template('contents/editProveedor.html',form=frm,datos=res)
    else :
        return redirect(url_for('index'))

@app.route('/proveedores/actualizar/<string:id>',methods=["PUT","POST"])
def actualizarProveedor(id):
    if 'userName' and 'name' in session :
        frm = FormPart()
        #recuperacion de datos proveedor
        nombresProveedor = escape(request.form['nombresProveedor'].strip()).lower()
        tipo_documento = escape(request.form['tipo_documento'].strip()).lower()
        numero_documento = escape(request.form['numero_documento'].strip())
        emailProveedor = escape(request.form['email'].strip())
        celularProveedor = escape(request.form['celular'].strip())
        direccionProveedor = escape(request.form['direccion'].strip())
        activo = 'si'
        logoProveedor = frm.logo.data
        if logoProveedor :
            nameImg = secure_filename(logoProveedor.filename)
            jinjaStart = "img/uploads/"
            urlImg = jinjaStart+nameImg
            logoSave = f"static/img/uploads/{nameImg}"
            logoProveedor.save(logoSave)

        if nombresProveedor and tipo_documento and numero_documento and emailProveedor and celularProveedor and direccionProveedor :
            #preparacion de sql
            sql = f"UPDATE proveedores SET nombresProveedor = ?, tipoDocumento = ?,numeroDocumento = ?,celularProveedor = ?,emailProveedor = ?,direccionProveedor = ?,activo =? WHERE id = {id} "
            #insertando los datos
            res = consult_action(sql,(nombresProveedor,tipo_documento, numero_documento,celularProveedor,emailProveedor,direccionProveedor,activo))
            if logoProveedor :
                producto_id = 0
                sql2 = f"UPDATE img SET nombreImg = ?,idProducto = ? WHERE idProveedores = {id} "
                res2 = consult_action(sql2,(urlImg,producto_id))
            else :
                res2 = 1

            if res!=0 and res2 != 0:
                flash('Proveedor actualizado con éxito ')
            else : 
                flash('Proveedor no registrado con éxito ')
            return redirect(url_for('proveedores'))
        else :
            flash('Fallo el registro faltaron campos por diligenciar')
            return redirect(url_for('formProveedor'))
    else :
        return redirect(url_for('index'))

@app.route('/proveedores/search/',methods=["GET","POST"])
def searchProveedores():
    if 'userName' and 'name' in session :
        atributo = escape(request.form['atributo'])
        valor = escape(request.form['valor']).lower()
        sql =  f'SELECT * FROM proveedores INNER JOIN img ON proveedores.id = img.idProveedores WHERE {atributo} LIKE "%{valor}%"'
        res = consult_select(sql)
        if len(res)!= 0 :
            return render_template('contents/proveedores.html', data=res)
        else : 
            return render_template('contents/proveedores.html', message='Sin resultados ')
    else :
        return redirect(url_for('index'))

@app.route('/proveedores/delete/<string:id>',methods=["GET","POST","PUT"])
def deleteProveedor(id):
    if 'userName' and 'name' in session :
        sql =  f"SELECT nombresProveedor, activo FROM proveedores WHERE id = {id}"
        res = consult_select(sql)
        name = res[0][0]
        if res[0][1] == 'si' :
            activo = 'no'
        else :
            activo = 'si'

        sql = f"UPDATE proveedores SET nombresProveedor =?, activo =? WHERE id = {id} "
        res = consult_action(sql,(name,activo))
        return redirect(url_for('proveedores'))
    else :
        return redirect(url_for('index'))



# URLS Productos

@app.route('/productos',methods=["GET"])
def productos():
    return render_template('contents/productos.html')


@app.route('/form/crear/producto/',methods=["GET"])
def formProducto():
    if 'userName' and 'name' in session :
        frm = FormPart()
        return render_template('contents/formProducto.html',form=frm)
    else :
        return redirect(url_for('index'))

@app.route('/producto/crear',methods=["POST"])
def crearProducto():
    if 'userName' and 'name' in session :
        frm = FormPart()
        #funcion para Guardar Imagenes en el Servidor
        def saveImgs(img) :
            nameImg = secure_filename(img.filename)
            jinjaStart = "img/uploads/"
            urlImg = jinjaStart+nameImg
            logoSave = f"static/img/uploads/{nameImg}"
            img.save(logoSave)

        #recuperacion de datos proveedor
        nombresProducto = escape(request.form['nombresProducto'].strip()).lower()
        descripcionProducto = escape(request.form['descripcion'].strip()).lower()
        cantidadMinima = escape(request.form['cantidadMinima'].strip())
        cantidadDisponible = escape(request.form['cantidadDisponible'].strip())
        activo = 'si'
        imgProducto1 = frm.img1.data
        imgProducto2 = frm.img2.data
        imgProducto3 = frm.img3.data
        if imgProducto1 :
            saveImgs(imgProducto1)
        if imgProducto2 :
            saveImgs(imgProducto2)
        if imgProducto3 :
            saveImgs(imgProducto3)
        return redirect(url_for('productos'))
        """
        if nombresProducto  and cantidadMinima :
            #preparacion de sql
            sql = "INSERT INTO Productoes(nombresProducto,tipoDocumento,numeroDocumento,celularProducto,emailProducto,direccionProducto,activo) VALUES (?,?,?,?,?,?,?) "
            #insertando los datos
            res = consult_action(sql,(nombresProducto,descripcionProducto, cantidadMinima,celularProducto,emailProducto,direccionProducto,activo))
            sql2 = "SELECT id FROM Productoes ORDER BY id DESC LIMIT 1"
            res2 = consult_select(sql2)
            Producto_id = res2[0][0]
            producto_id = 0
            sql3 = "INSERT INTO img(nombreImg,idProducto,idProductoes) VALUES (?,?,?) "
            res3 = consult_action(sql3,(urlImg,producto_id, proveedor_id))

            if res!=0 and res2 != None and res3!=0:
                flash('Proveedor registrado con éxito ')
            else : 
                flash('Proveedor no registrado con éxito ')
            return redirect(url_for('proveedores'))
        else :
            flash('Fallo el registro faltaron campos por diligenciar')
            return redirect(url_for('formProveedor')) """
    else :
        return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(port=8080, debug=True)