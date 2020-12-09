__all__ = ["User", "Task", "AppSession", "Folder", "ServerSetting"]
from utility.HttpException import HttpException, HttpErrorType

connectionString = "mysql+mysqlconnector://root:@localhost:3306/testdb"

from sqlalchemy import create_engine
engine = create_engine(connectionString, echo=False)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
# session = Session()

from contextlib import contextmanager
@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()