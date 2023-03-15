from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite+pysqlite:///gametools.db', echo=True)
session = Session(engine)
Base = declarative_base()
Base.metadata.create_all(engine)
