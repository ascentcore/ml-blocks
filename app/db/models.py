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
    
    id = Column(Integer, primary_key=True)    
    state = Column(Integer, nullable=False)
    state_name = Column(String(256), nullable=False)
    time = Column(DateTime(timezone=True), default=func.now())