import os
import logging
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv
from db_map import Base, Training
from datetime import datetime

load_dotenv()


engine = create_engine(f'sqlite:///{os.getenv("DB_FILENAME")}')


if not os.path.isfile(f'./{os.getenv("DB_FILENAME")}'):
    Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()
newItem = Training(chat_id="0", text_message="", date=datetime.now(), reply_sent=True, deleted=True, )
try:
    session.add(newItem)
    session.commit()
except Exception as e:
    logging.error(
        'Couldn\'t upload {}. Error is {}')
else:
    logging.info(
        f'Successfully uploaded and saved to DB file ')
finally:
    session.close()

