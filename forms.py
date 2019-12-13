from wtforms import Form, FormField, IntegerField, SubmitField, validators, StringField, PasswordField

class LoginForm(Form):
    username = StringField('Usuario', [
        validators.Required(message='Usuario requerido.'),
        validators.length(min=4, max=30, message='Nombre de usuario no valido.'),
    ])
    password = PasswordField('Password', [validators.Required(message = 'La contraseña es requerida')])

class ActionsForm(Form):
    stop = SubmitField(id="stop")
    reset = SubmitField(id="reset")

class CyclesForm(Form):
    cycles = IntegerField(id='Número de ciclos',validators=[
                                  validators.NumberRange(min=1, max=10**9, message='Introduce un entero mayor que 0'),
                                  validators.Optional(True),
                                  ])                   
    submit = SubmitField(id="start")

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