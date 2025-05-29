from typing import Annotated

from fastapi import Depends

from application.database import SessionLocal, get_db

Session = Annotated[SessionLocal, Depends(get_db)]


class Repository:
    def __init__(self, db_session: Session = Depends(get_db)):
        self.db = db_session
