from wtforms import Form, StringField, PasswordField, validators

class RegForm(Form):
    username = StringField('Username', [
        validators.InputRequired(), 
        validators.Length(min=5, max=32, message='Login must contain between 5 and 32 symbols')
        ])
    password = PasswordField('New Password', [
        validators.InputRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),
        validators.Length(min=8, max=32, message='Password must contain between 8 and 32 symbols')
        ])
    confirm = PasswordField('Repeat Password',[
        validators.InputRequired()
        ])


class LogForm(Form):
    username = StringField('Username', [
        validators.InputRequired(), 
        validators.Length(min=5, max=32, message='Login must contain between 5 and 32 symbols')
        ])
    password = PasswordField('Password', [
        validators.InputRequired(),
        validators.Length(min=8, max=32, message='Password must contain between 8 and 32 symbols')
        ])
    

class SongForm(Form):
    name = StringField('Title', [
        validators.InputRequired(),
        validators.Length(max=1000, message='Song title must contain up to 1000 symbols')
    ])
    album = StringField('Album', [
        validators.InputRequired(),
        validators.Length(max=1000, message='Album title must contain up to 1000 symbols')
    ])
    artist = StringField('Artist', [
        validators.InputRequired(),
        validators.Length(max=1000, message='Artist name must contain up to 1000 symbols')
    ])
    