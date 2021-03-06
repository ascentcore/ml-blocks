from .models import  Status, Graph
from app.constants import stages

def set_status(db, status):
    status = Status(state = stages[status], state_name=status)
    db.add(status)
    db.commit()
    db.refresh(status)

    return status

def get_graph(db):
    return db.query(Graph).all()

def get_status(db):
    return db.query(Status).order_by(Status.id.desc()).first()


def cleanup(db):    
    db.query(Graph).delete()    
    db.query(Status).delete()