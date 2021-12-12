import  os
from    sqlalchemy                 import create_engine
from    sqlalchemy.orm             import sessionmaker
from    sqlalchemy.ext.declarative import declarative_base

#result = os.environ.get('jdbc:postgresql://localhost:5432/postgres')
engine = create_engine("postgresql://postgres:98684@localhost:5432/postgres")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()