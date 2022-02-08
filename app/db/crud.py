from .models import Dependency, Status, Graph
from app.constants import stages

def set_status(db, status):
    status = Status(state = stages[status], state_name=status)
    db.add(status)
    db.commit()
    db.refresh(status)

    return status


def get_status(db):
    return db.query(Status).order_by(Status.id.desc()).all()


def get_dependencies(db):
    return db.query(Dependency).all()


def cleanup(db):    
    db.query(Dependency).delete()
    db.query(Graph).delete()    
    db.query(Status).delete()