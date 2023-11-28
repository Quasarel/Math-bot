from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Settings(Base):
    __tablename__ = 'Settings'
    tg_id = Column(Integer, primary_key=True)
    timer_limit = Column(Integer)
