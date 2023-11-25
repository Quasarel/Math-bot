import os
import logging
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine, Engine, event
from sqlalchemy.orm import scoped_session, sessionmaker, DeclarativeBase
from dotenv import load_dotenv
from database.db_map import Base, Settings

from datetime import datetime

load_dotenv()


engine = create_engine(f'sqlite:///{os.getenv("DB_FILENAME")}')

Session = sessionmaker(engine)

if not os.path.isfile(f'./{os.getenv("DB_FILENAME")}'):
    Base.metadata.create_all(engine)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class Base(DeclarativeBase):
    pass

# session_factory = sessionmaker(bind=engine)
# Session = scoped_session(session_factory)
# session = Session()
# newItem = Training(chat_id="0", text_message="", date=datetime.now(), reply_sent=True, deleted=True, )
# try:
#     session.add(newItem)
#     session.commit()
# except Exception as e:
#     logging.error(
#         'Couldn\'t upload {}. Error is {}')
# else:
#     logging.info(
#         f'Successfully uploaded and saved to DB file ')
# finally:
#     session.close()

