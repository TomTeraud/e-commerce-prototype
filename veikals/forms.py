from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, DecimalField, FileField, TextAreaField
from wtforms.validators import ValidationError, InputRequired, Length, Email, EqualTo, DataRequired, NumberRange
from veikals.models import User


class PasutijumaForm(FlaskForm):
    email = StringField('E-pasts', validators=[InputRequired(), Email()])
    vards = StringField('Vārds')#, validators=[InputRequired()])
    uzvards = StringField('Uzvārds')#, validators=[InputRequired()])
    telefons = StringField('Telefons')#, validators=[InputRequired()])
    valsts = SelectField('Valsts', choices=['Latvija', 'Lietuva', 'Igaunija'], validators=[DataRequired()])
    pilseta = StringField('Pilsēta')#, validators=[InputRequired()])
    adrese = StringField('Adrese')#, validators=[InputRequired()])
    pasta_index = StringField('Pasta indekss')#, validators=[InputRequired()])
    submit = SubmitField('Turpināt')


class RegistrationForm(FlaskForm):
    username = StringField('lietotajvards', validators=[InputRequired()])
    email = StringField('E-pasts', validators=[InputRequired(), Email()])
    password = PasswordField('Parole', validators=[InputRequired()])
    password2 = PasswordField(
        'Atkārtot paroli', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Reģistrēties')

    # validates username availability in database
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Lietotajvārds nav pieejams.')
    
    # validates email availability in database
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Šis email ir aizņemts.')


class LoginForm(FlaskForm):
    username = StringField('Lietotajvārds', validators=[DataRequired()])
    password = PasswordField('Parole', validators=[DataRequired()])
    remember_me = BooleanField('Atcerēties mani')
    submit = SubmitField('Pieslēgties')


class SelectPreceForm(FlaskForm):
    select_prece_form = SelectField('Izvēlēties preces pēc id vai artikula', choices=[], validators=[DataRequired()])
    select = SubmitField('Apstiprināt izvēli')


class AddPreceForm(FlaskForm):
    klase = SelectField('Klase', choices=['berniem', 'sievietem', 'viriesiem'])
    grupa = SelectField('Grupa', choices=[
        'ratiem', 
        'apgerbs', 
        'somas', 
        'atstarojosas-vestes'
        ])
    veids = SelectField('Veids', choices=[
        'atstarojosas-vestes', 
        'cimdi', 
        'gurnu-somas',
        'gulammaiss', 
        'lietus-pleve', 
        'lietus-bikses', 
        'lietus-meteli',
        'mugursomas', 
        'moskitu-tikli', 
        'kombinzoni', 
        'kreklini', 
        'rudens-pavasara-apgerbs', 
        'softshell-kombinzoni', 
        'softshell-zabacini', 
        'skolas-somas', 
        'softshell-virsjaka'
        ],validators=[InputRequired()])
    izejmateriali = TextAreaField('Izejmateriali', validators=[InputRequired(), Length(min=5, max=300)])
    apraksts = TextAreaField('Preces apraksts', validators=[InputRequired(), Length(min=5, max=500)])
    krasa = StringField('Krāsa', validators=[InputRequired(), Length(min=3, max=50)])
    izmers = StringField('Izmers', validators=[InputRequired(), Length(max=32)])
    cena = DecimalField('Preces cena', validators=[InputRequired()])
    

class AddBildeForm(FlaskForm):
    bildes = FileField('Pievienot bildes')
    submit = SubmitField('Pievienot bildi')


class EmptyForm(FlaskForm):
    submit = SubmitField('SUBMIT', render_kw={"class": "mdl-button mdl-js-button mdl-button--raised mdl-button--accent"})
    pievienot = SubmitField('+', render_kw={"class": "mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect mdl-button--colored"})


class PievienotPreciGrozamForm(FlaskForm):
    prece_id = IntegerField('prece_id')
    discount = IntegerField('Atlaide %', default=0, validators=[InputRequired(), NumberRange(min=0, max=100)])
    ielikt_groza = SubmitField('Ielikt grozā')


class EditPasutijumsForma(FlaskForm):
    edit_status = SelectField('Mainīt statusu', choices=['Gaida apmaksu', 'Ir apmaksāts','Tiek komplektēts', 'Nosūtīts pircējam'], validators=[DataRequired()])
    submit = SubmitField('Apstiprināt statusa izmaiņas')
    delete_pasutijums = SubmitField('Izdzēst pasūtījumu')