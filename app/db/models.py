from sqlalchemy import Column, Integer, String

from app.db.base_class import Base

class Dependency(Base): 
    __tablename__ = 'dependency'

    id = Column(Integer, primary_key=True, index=True) 
    dependency = Column(String(256), nullable=False)
