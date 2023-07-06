from datetime import datetime
from veikals import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.associationproxy import association_proxy



class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), index=True, unique=True)
    username = db.Column(db.String(64), unique=True)
    vards = db.Column(db.String(64))
    uzvards = db.Column(db.String(64))
    telefons = db.Column(db.String(64))
    valsts = db.Column(db.String(64))
    pilseta = db.Column(db.String(64))
    adrese = db.Column(db.String(128))
    pasta_index = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))


    pasutijumi = db.relationship("Pasutijums", back_populates="user")

    def __repr__(self):
        return '<User:{} id:{}>'.format(self.username, self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

     
class AnonimUser(UserMixin, db.Model):
    __Tablename__ = 'anonim_user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), index=True)
    uzvards = db.Column(db.String(64))
    vards = db.Column(db.String(64))
    telefons = db.Column(db.String(64))
    valsts = db.Column(db.String(64))
    pilseta = db.Column(db.String(64))
    adrese = db.Column(db.String(128))
    pasta_index = db.Column(db.String(64))

    pasutijumi = db.relationship("Pasutijums", back_populates="anonim_user")

class Bilde(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bilde_name = db.Column(db.String(128))
    bilde_url = db.Column(db.String(128))
    thumbnail_url = db.Column(db.String(128))
    prece_id = db.Column(db.Integer)
    prece = db.relationship("Prece", back_populates="bildes")


class Pasutijums(db.Model):
    __tablename__ = "pasutijums"
    id = db.Column(db.Integer, primary_key=True)
    pasutijuma_datums = db.Column(db.DateTime, nullable=False, default=datetime.now())
    summa = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(50), default='Gaida apmaksu')
    
    
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    anonim_user_id = db.Column(db.Integer, db.ForeignKey("anonim_user.id"))

    user = db.relationship("User", back_populates="pasutijumi")
    anonim_user = db.relationship("AnonimUser", back_populates="pasutijumi")
    preces_association = db.relationship("PasutijumsPrece", back_populates="pasutijums", cascade="all, delete")
    preces = association_proxy("preces_association", "prece")

    def __init__(self, anonim_user_id, pasutijuma_datums):
        self.anonim_user_id = anonim_user_id
        self.pasutijuma_datums = pasutijuma_datums
        
    
class Prece(db.Model):
    __Tablename__ = 'prece'
    id = db.Column(db.Integer, primary_key=True)
    artikuls = db.Column(db.String(16))
    cena = db.Column(db.Float, nullable=False)
    izejmateriali = db.Column(db.String(300))
    apraksts = db.Column(db.String(500))
    krasa = db.Column(db.String(50))
    izmers = db.Column(db.String(32))
    klase = db.Column(db.String(50))
    grupa = db.Column(db.String(50))
    veids = db.Column(db.String(50))
    titulbildes_id = db.Column(db.Integer, db.ForeignKey("bilde.id"))
    titulbildes_url = db.Column(db.String(128))

    bildes = db.relationship("Bilde", back_populates="prece", cascade="all, delete")
    

class PasutijumsPrece(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artikuls = db.Column(db.String(16))
    cena = db.Column(db.Float)
    cena_ar_atlaidi = db.Column(db.Float)
    atlaide = db.Column(db.Float)
    veids = db.Column(db.String(50))
    grupa = db.Column(db.String(50))
    klase = db.Column(db.String(50))
    izmers = db.Column(db.String(32))
    krasa = db.Column(db.String(50))
    pasutijums_id = db.Column(db.Integer, db.ForeignKey("pasutijums.id"))
    
    pasutijums = db.relationship("Pasutijums", back_populates="preces_association")
    
    def __init__(self, pasutijums, prece, cena=None):
        self.prece = prece
        self.pasutijums = pasutijums
        self.cena = cena or prece.cena
        self.cena_ar_atlaidi = cena or prece.cena
        self.atlaide = 0
        self.artikuls = prece.artikuls
        self.veids = prece.veids
        self.grupa = prece.grupa
        self.klase = prece.klase
        self.izmers = prece.izmers
        self.krasa = prece.krasa


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
