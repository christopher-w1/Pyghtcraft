from sqlalchemy import Column, Integer, String, Float, BigInteger, DateTime
from . import Base

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