from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Settings(Base):
    __tablename__ = 'Settings'
    tg_id = Column(Integer, primary_key=True)
    timer_limit = Column(Integer)
    # text_message = Column(String(255))
    # date = Column(Date)
    # reply_sent = Column(Boolean)
    # deleted = Column(Boolean)
