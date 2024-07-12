from sqlalchemy import Column, Integer, BigInteger

from data.base import Base


class GamerScore(Base):
    __tablename__: str = "gamer_score"
    user_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    score = Column(Integer, default=0)
