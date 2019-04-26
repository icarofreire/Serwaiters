from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

DB_URI = 'sqlite:///./main.db'
Session = sessionmaker(autocommit=False, autoflush=False, bind=create_engine(DB_URI))
session = scoped_session(Session)
