from wtforms import Form, FormField, IntegerField, SubmitField, BooleanField, validators, StringField, PasswordField
from models import User

class LoginForm(Form):
    username = StringField('Usuario', [
        validators.Required(message='Usuario requerido.'),
        validators.length(min=4, max=30, message='Nombre de usuario no valido.'),
    ])
    password = PasswordField('Password', [validators.Required(message = 'La contraseña es requerida')])

class CreateForm(Form):
    admin = BooleanField('Administrador', [validators.Optional(True)])
    username = StringField('Usuario', [
        validators.Required(message='Usuario requerido.'),
        validators.length(min=4, max=30, message='Nombre de usuario no valido.'),
    ])
    password = PasswordField('Password', [validators.Required(message = 'La contraseña es requerida')])

    def validate_username(self, form, field):
        username = field.data
        user = User.query.filter_by(username = username).first()
        if user != None:
            raise validators.ValidationError('El nombre de usuario ya se encuentra registrado.')

class ActionsForm(Form):
    pass

class CyclesForm(Form):
    cycles = IntegerField(id='Número de ciclos',validators=[
                                  validators.NumberRange(min=1, max=10**9, message='Introduce un entero mayor que 0'),
                                  validators.Optional(True),
                                  ])      

class PanelForms(Form):
    cyclesForm = FormField(CyclesForm)
    actionsForm = FormField(ActionsForm)
    
    def action(self):
        if self.cyclesForm.submit.data:
            return "start"
        elif self.actionsForm.stop.data:
            return "stop"
        elif self.actionsForm.reset.data:
            return "reset"