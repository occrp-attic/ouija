import yaml
from sqlalchemy import create_engine, MetaData

from ouija.core import app
from ouija.model.database import OuijaDatabase, OuijaTable, OuijaColumn
from ouija.model.query import OuijaQuery, OuijaQueryException

__all__ = [OuijaDatabase, OuijaTable, OuijaColumn, OuijaQuery,
           OuijaQueryException]

engine = create_engine(app.config.get('DATABASE_URI'))
meta = MetaData(bind=engine)
meta.reflect(engine)
config = yaml.load(open(app.config.get('TABLES_CONFIG'), 'rb'))

db = OuijaDatabase(engine, meta, config)
