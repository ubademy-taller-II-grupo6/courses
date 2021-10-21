import  os
from    sqlalchemy                 import create_engine
from    sqlalchemy.orm             import sessionmaker
from    sqlalchemy.ext.declarative import declarative_base

result = os.environ.get('DATABASE_URL')
engine = create_engine(result)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()