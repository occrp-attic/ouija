import yaml
from sqlalchemy import create_engine, MetaData

from ouija.core import app
from ouija.model.database import OuijaDatabase

engine = create_engine(app.config.get('DATABASE_URI'))
meta = MetaData(bind=engine)
meta.reflect(engine)
config = yaml.load(open(app.config.get('TABLES_CONFIG'), 'rb'))

db = OuijaDatabase(engine, meta, config)
