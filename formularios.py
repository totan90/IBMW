from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, validators, SubmitField, SelectField, RadioField
from markupsafe import Markup
from wtforms.validators import InputRequired , Regexp
from wtforms.fields.html5 import EmailField

class Login(FlaskForm):
    username_value = Markup('<span class="input-group-text" id="basic-addon1"><i class="fas fa-user-tie p-2"></i>Usuario</span>')
    username = TextField(username_value,validators = [InputRequired(message='Campo obligatorio'),validators.Regexp('\w+', flags=0, message='caracteres no permitidos')])
    password_value = Markup('<span class="input-group-text" id="basic-addon1"><i class="fas fa-key p-2"></i>Contraseña</span>')

    password = PasswordField(password_value, validators = [InputRequired(message='Campo obligatorio')])

    ingresar = SubmitField('Ingresar')

class FormPart(FlaskForm):

    nombres = TextField('Nombres',validators = [InputRequired(message='Campo obligatorio'),validators.Regexp('/^[A-Za-z0-9\s]+$/g', flags=0, message='caracteres no permitidos')])
    apellidos = TextField('Apellidos',validators = [InputRequired(message='Campo obligatorio'),validators.Regexp('/^[A-Za-z0-9\s]+$/g', flags=0, message='caracteres no permitidos')])
    tipo_documento = RadioField('Tipo Documento', choices=[('C.C','C.C'),('T.I','T.I'),('C.E','C.E')],default='C.C')
    numero_documento = TextField('No Documento',validators = [InputRequired(message='Campo obligatorio'),validators.Regexp('/^[A-Za-z0-9\s]+$/g', flags=0, message='caracteres no permitidos')])
    email = EmailField('Email',validators = [InputRequired(message='Campo obligatorio'),validators.Regexp("^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$", flags=0, message='correo no valido')])
    celular = TextField('Celular',validators = [InputRequired(message='Campo obligatorio'),validators.Regexp('^(\d{10})$', flags=0, message='caracteres no permitidos')])
    direccion = TextField('Dirección',validators = [InputRequired(message='Campo obligatorio')],default='ingrese la dirección')
    username = TextField('Nombre de Usuario',validators = [InputRequired(message='Campo obligatorio'),validators.Regexp('\w+', flags=0, message='caracteres no permitidos')])
    password = PasswordField('Contraseña', validators = [InputRequired(message='Campo obligatorio'),validators.Regexp('^(?=\w*\d)(?=\w*[A-Z])(?=\w*[a-z])\S{8,16}$', flags=0, message='caracteres no permitidos')])
    confirm_password = PasswordField('Confirmar Contraseña', validators = [InputRequired(message='Campo obligatorio'),validators.Regexp('^(?=\w*\d)(?=\w*[A-Z])(?=\w*[a-z])\S{8,16}$', flags=0, message='caracteres no permitidos')])
    roles = SelectField('Asignar Rol', choices=[(1,'Administrador'), (2,'Super Administrador'),(3,'Usuario Final') ],default=3)
    autorizacion = RadioField('Autorizacion de Datos', choices=[('si','Autorizo el manejo y almacenamiento de datos personales')],default='si')
    crear = SubmitField('Crear Usuario')
    actualizar = SubmitField('Actualizar Usuario')
