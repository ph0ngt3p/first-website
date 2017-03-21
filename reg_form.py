from wtforms import Form, BooleanField, TextField, PasswordField, validators

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50), validators.Email(message = 'Please enter a valid email.')])
    password = PasswordField('New Password', [
    	validators.Length(min=6, max=20),
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat password')
    accept_tos = BooleanField('I accept the Terms of Service and blahbloh', [validators.Required()])