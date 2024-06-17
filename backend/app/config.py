import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from dotenv import load_dotenv
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")

SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


SECRET_KEY     = os.getenv("SECRET_KEY")
HASH_ALGORITHM = "HS256"
SUPERADMIN_PASSWORD = os.getenv("SUPERADMIN_PASSWORD")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
HASHED_SUPERADMIN_PASSWORD = pwd_context.hash(SUPERADMIN_PASSWORD)

engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()