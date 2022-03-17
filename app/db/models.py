from sqlalchemy import Column, Integer, String, func, DateTime

from app.db.base_class import Base


class Block(Base): 
    __tablename__ = 'block'
    host = Column(String(256), nullable=False, primary_key=True)
    name = Column(String(256), nullable=True)

class Graph(Base): 
    __tablename__ = 'graph'
    id = Column(Integer)    
    upstream = Column(String(256), nullable=False, primary_key=True)
    downstream = Column(String(256), nullable=False, primary_key=True)
    edge_type = Column(Integer, nullable=False, primary_key=True)

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


class Report(Base):
    __tablename__ = 'report'
    
    host = Column(String(256), nullable=False, primary_key=True)
    type = Column(String(256), nullable=False, primary_key=True)
    value = Column(String(256), nullable=False)