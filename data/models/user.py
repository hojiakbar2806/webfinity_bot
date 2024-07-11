from sqlalchemy import BigInteger, Column, Float, Integer, String
from data.base import Base


class User(Base):
    __tablename__: str = 'users'
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(BigInteger, unique=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    gender = Column(String)
    profile_pic = Column(String, nullable=True)
