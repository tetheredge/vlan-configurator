from sqlalchemy import create_engine

import os
import credentials
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager

creds = credentials.Credentials()
db_name = creds.get_db_name()
db_password = creds.get_db_password()
db_user = creds.get_db_user()
db_host = creds.get_db_hostname()
db_port = creds.get_db_port()

db_uri = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

DATABASE_URI = os.getenv('TEST_DB', db_uri)
engine = create_engine(DATABASE_URI, pool_size=2, isolation_level="AUTOCOMMIT")
engine.dispose()
Session = scoped_session(sessionmaker())

session = Session(bind=engine)

@contextmanager
def session_scope():
    engine.dispose()
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
        engine.dispose()