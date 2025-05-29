from sqlalchemy.orm import Session

from application.database import get_db


class Repository:
    def __init__(self, db: Session = next(get_db())):
        self.db = db
