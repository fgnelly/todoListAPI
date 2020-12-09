__all__ = ["User", "Task", "AppSession", "Folder", "ServerSetting"]
from utility.HttpException import HttpException, HttpErrorType

from utility import Config
serverConfig = Config.Get('server-config.xml')
if serverConfig is None:
    print('Could not load server config, check if tags are correct and the file exists.')
    exit()

connectionString = 'mysql+mysqlconnector://{0}:{1}@{2}/{3}'.format(
    serverConfig['databaseUser'],
    serverConfig['databasePassword'] if serverConfig['databasePassword'] is not None else "",
    serverConfig['databaseServer'],
    serverConfig['databaseName']
)

from sqlalchemy import create_engine
engine = create_engine(connectionString, echo=False)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)

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