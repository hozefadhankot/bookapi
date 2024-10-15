from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.cred import Cred

user = Cred.psql["username"]
password = Cred.psql["password"]
host = Cred.psql["host"]
port = Cred.psql["port"]
database = Cred.psql["database"]

# Correct connection URL
DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{database}"
# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our models
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
