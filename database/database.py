import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from database.db_map import Base

load_dotenv()


engine = create_engine(f'sqlite:///{os.getenv("DB_FILENAME")}')

Session = sessionmaker(engine)

if not os.path.isfile(f'./{os.getenv("DB_FILENAME")}'):
    Base.metadata.create_all(engine)
