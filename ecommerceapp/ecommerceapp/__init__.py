from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import BaseConfig
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from . import routes, models    


#do not delete these below methods
@app.cli.command()
def erasedata():
    db.drop_all()
    db.session.commit()
    db.create_all()
@app.cli.command()
def seeddata():
    from . import seed
