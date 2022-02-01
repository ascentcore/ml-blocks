from sqlalchemy import Column, Integer, String, func, DateTime

from app.db.base_class import Base

class Dependency(Base): 
    __tablename__ = 'dependency'

    dependency = Column(String(256), primary_key=True, nullable=False)

class Settings(Base):
    __tablename__ = 'settings'

    name = Column(String(256), nullable=False, primary_key=True)
    value = Column(String(256), nullable=True)


class Status(Base):
    __tablename__ = 'status'

    state = Column(String(256), nullable=False, primary_key=True)
    time = Column(DateTime(timezone=True), onupdate=func.now())