import datetime

from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UserExcelData(Base):
    __tablename__ = 'user_excel_table'

    id = Column(Integer, primary_key=True, index=True)
    user = Column(Integer, index=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    xpath = Column(String, nullable=False)
    price = Column(Float, nullable=True)
    added_at = Column(DateTime, default=datetime.datetime.now())
