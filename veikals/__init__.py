from flask import Flask
from config import Config, Savienojums
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from datetime import timedelta
from veikals.helpers import usd, eur, discount


app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd
app.jinja_env.filters["eur"] = eur
app.jinja_env.filters["discount"] = discount

app.config.from_object(Savienojums)
app.config.from_object(Config)
app.permanent_session_lifetime = timedelta(days=3)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

#csrf = CSRFProtect(app) #need setup bildes upload formai, to use csrf token



from veikals import routes, models, errors, helpers