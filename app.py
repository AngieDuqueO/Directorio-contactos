from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Contacto, Cuenta
from forms import ContactForm, AccountForm
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['SECRET_KEY'] = 'developer123'
csrf = CSRFProtect(app)

db.init_app(app)  # Inicializar la base de datos

class DeleteForm(FlaskForm):
    pass

#Ruta index
@app.route('/')
def index():
    contacts = Contacto.query.all()
    delete_form = DeleteForm()
    return render_template('index.html', contacts=contacts, form=delete_form)

#Ruta creacion de contactos
@app.route('/contacto/nuevo', methods=['GET', 'POST'])
def create_contact():
    form = ContactForm()
    form.id_cuenta.choices = [(a.id, a.nombre_cuenta) for a in Cuenta.query.all()]

    if form.validate_on_submit():
        new_contact = Contacto(
            nombres=form.nombres.data,
            apellidos=form.apellidos.data,
            tipo_documento=form.tipo_documento.data,
            numero_documento=form.numero_documento.data,
            fecha_nacimiento=form.fecha_nacimiento.data,
            email=form.email.data,
            numero_celular=form.numero_celular.data,
            numero_fijo=form.numero_fijo.data,
            tipo_contacto=form.tipo_contacto.data,
            id_cuenta=form.id_cuenta.data,
            valor_descuento=form.valor_descuento.data
        )
        db.session.add(new_contact)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('formulario_contacto.html', form=form)

#Ruta para la edicion de contactos con validacion de duplicado
@app.route('/contacto/editar/<int:id>', methods=['GET', 'POST'])
def edit_contact(id):
    contact = Contacto.query.get_or_404(id)
    form = ContactForm(obj=contact)  # Precarga los datos del contacto
    form.id_cuenta.choices = [(a.id, a.nombre_cuenta) for a in Cuenta.query.all()]  # Opciones dinámicas

    if form.validate_on_submit():
        
        # Actualizar datos
        contact.nombres = form.nombres.data
        contact.apellidos = form.apellidos.data
        contact.tipo_documento = form.tipo_documento.data
        contact.numero_documento = form.numero_documento.data
        contact.fecha_nacimiento = form.fecha_nacimiento.data
        contact.email = form.email.data
        contact.numero_celular = form.numero_celular.data
        contact.numero_fijo = form.numero_fijo.data
        contact.tipo_contacto = form.tipo_contacto.data
        contact.id_cuenta = form.id_cuenta.data
        contact.valor_descuento = form.valor_descuento.data
        db.session.commit()
        flash('Contacto actualizado exitosamente', 'success')
        return redirect(url_for('index'))
    
    return render_template('editar_contacto.html', form=form)

#Ruta para eliminar contactos existentes
@app.route('/contacto/eliminar/<int:id>', methods=['POST'])
def delete_contact(id):
    form = DeleteForm()
    if form.validate_on_submit():  # Validar el token CSRF
        try:
            contact = Contacto.query.get_or_404(id)
            db.session.delete(contact)
            db.session.commit()
            flash('Contacto eliminado exitosamente', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al eliminar contacto: {str(e)}', 'error')
    else:
        flash('Solicitud no válida o token CSRF incorrecto.', 'error')
    return redirect(url_for('index'))

#Ruta para la creacion y consulta de cuentas maestras
@app.route('/cuenta_maestra', methods=['GET', 'POST'])
def create_account():
    form = AccountForm()
    delete_form = DeleteForm()
    accounts = Cuenta.query.all()
    
    if form.validate_on_submit():
        try:
            new_account = Cuenta(
                codigo=form.code.data,
                numero_cuenta=form.numero_cuenta.data,
                nombre_cuenta=form.nombre_cuenta.data,
                tipo_cuenta=form.tipo_cuenta.data
            )
            db.session.add(new_account)
            db.session.commit()
            flash('Cuenta creada exitosamente.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la cuenta: {str(e)}', 'error')

    return render_template('cuenta_maestra.html', form=form, delete_form=delete_form, accounts=accounts)

@app.route('/cuenta/editar/<int:id>', methods=['GET', 'POST'])
def edit_account(id):
    cuenta = Cuenta.query.get_or_404(id)  # Obtener la cuenta por su ID
    form = AccountForm(obj=cuenta)  # Precargar los datos de la cuenta

    if form.validate_on_submit():
        cuenta.codigo = form.code.data
        cuenta.numero_cuenta = form.numero_cuenta.data
        cuenta.nombre_cuenta = form.nombre_cuenta.data
        cuenta.tipo_cuenta = form.tipo_cuenta.data
        db.session.commit()
        flash('Cuenta actualizada exitosamente', 'success')
        return redirect(url_for('create_account'))

    return render_template('editar_cuenta_maestra.html', form=form)


#Ruta para eliminar cuentas maestras especificas
@app.route('/cuenta/eliminar/<int:id>', methods=['POST'])
def delete_account(id):
    form = DeleteForm()
    if form.validate_on_submit():  # Validar el token CSRF
        try:
            cuenta = Cuenta.query.get_or_404(id)
            db.session.delete(cuenta)
            db.session.commit()
            flash('Cuenta eliminada exitosamente', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al eliminar cuenta: {str(e)}', 'error')
    else:
        flash('Solicitud no válida o token CSRF incorrecto.', 'error')
    return redirect(url_for('create_account'))

#Ruta para consultar registros en la base de datos sobre las cuentas maestras
@app.route('/debug/cuentas_detalle')
def debug_accounts_detail():
    try:
        # Verificar si la tabla existe
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        # Obtener todas las cuentas
        accounts = Cuenta.query.all()
        
        # Preparar la respuesta
        response = {
            'tablas_en_db': tables,
            'numero_de_cuentas': len(accounts),
            'cuentas': [],
            'estructura_tabla': {
                'columnas': [c['name'] for c in inspector.get_columns('cuentas')]
            }
        }
        
        # Agregar detalles de cada cuenta
        for account in accounts:
            account_data = {
                'id': account.id,
                'codigo': account.codigo,
                'numero_cuenta': account.numero_cuenta,
                'nombre_cuenta': account.nombre_cuenta,
                'tipo_cuenta': account.tipo_cuenta
            }
            response['cuentas'].append(account_data)
        
        return response
    except Exception as e:
        return {'error': str(e), 'tipo_error': type(e).__name__}
    
if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()  # Crea las tablas si no existen
    app.run(host='127.0.0.1', port=5002, debug=True)
