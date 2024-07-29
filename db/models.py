from sqlalchemy import Column, Integer, String, Float, BigInteger, DateTime
from . import Base

class Authentification(Base):
    __tablename__ = 'authentifications'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    realname = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    x = Column(Float, nullable=False, default=0.5)
    y = Column(Float, nullable=False, default=65.0)
    z = Column(Float, nullable=False, default=0.5)
    regdate = Column(BigInteger, nullable=False, default=0.5)
    regip = Column(String(40), nullable=False, default="0.0.0.0")
    email = Column(String(255), nullable=False)


class WebApiSession(Base):
    __tablename__ = 'webapi_session'
    username = Column(String(255), primary_key=True, nullable=False)
    api_key = Column(String(255), primary_key=True, nullable=False)
    valid_until = Column(DateTime, nullable=False)
    perm_level = Column(Integer, nullable=False)


class WebsitePermissions(Base):
    __tablename__ = 'website_permissions'
    username = Column(String(255), primary_key=True, nullable=False)
    perm_level = Column(Integer, nullable=False)