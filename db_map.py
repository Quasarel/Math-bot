from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Training(Base):
    __tablename__ = 'Training'
    id = Column(Integer, primary_key=True)
    chat_id = Column(String(20))
    text_message = Column(String(255))
    date = Column(Date)
    reply_sent = Column(Boolean)
    deleted = Column(Boolean)
