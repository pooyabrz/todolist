from sqlalchemy.orm import Session
from ..db.session import SessionLocal

<<<<<<< HEAD
def get_db():
=======
def get_db() -> Session:
>>>>>>> bc1d1638349c56f6913be85b56ccf55ab5d74a68
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()