from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from models import Contacto

# Validación personalizada para el correo
def validate_email_domain(form, field):
    if not field.data.endswith(".com"):
        raise ValidationError("El correo debe terminar en .com")

class ContactForm(FlaskForm):
    nombres = StringField('Nombres', validators=[DataRequired(), Length(max=100)])
    apellidos = StringField('Apellidos', validators=[DataRequired(), Length(max=100)])
    tipo_documento = SelectField('Tipo Doc.', choices=[('CC', 'Cédula'), ('NIT', 'NIT')], validators=[DataRequired()])
    numero_documento = StringField('Número de Identificación', validators=[DataRequired(), Length(max=50)])
    fecha_nacimiento = DateField('Fecha de Nacimiento', validators=[DataRequired()])
    email = StringField('Correo Personal', validators=[DataRequired(), Email(), validate_email_domain])
    numero_celular = StringField('Número Celular', validators=[DataRequired(), Length(max=15)])
    numero_fijo = StringField('Número Fijo', validators=[Length(max=15)])
    tipo_contacto = SelectField('Tipo Contacto', choices=[('Cliente', 'Cliente'), ('Proveedor', 'Proveedor')], validators=[DataRequired()])
    id_cuenta = SelectField('Cuenta Contable', coerce=int, validators=[DataRequired()])
    valor_descuento = IntegerField('Valor Descuento', validators=[DataRequired()])
    submit = SubmitField('Guardar')

class AccountForm(FlaskForm):
    code = StringField('Código', validators=[DataRequired()])
    numero_cuenta = StringField('Número de Cuenta', validators=[DataRequired()])
    nombre_cuenta = StringField('Nombre de la Cuenta', validators=[DataRequired()])
    tipo_cuenta = SelectField('Tipo de Cuenta', choices=[('Gasto', 'Gasto')], validators=[DataRequired()])
    submit = SubmitField('Guardar')
