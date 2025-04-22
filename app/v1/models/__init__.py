from datetime import datetime

import pytz
from sqlalchemy.orm import Mapped, as_declarative

from app.db.database import db


@as_declarative()
class Base(object):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)

    created_at: Mapped[datetime] = db.Column(
        db.DateTime(timezone=True), default=datetime.now(pytz.UTC), nullable=False
    )
    updated_at: Mapped[datetime] = db.Column(
        db.DateTime(timezone=True),
        default=datetime.now(pytz.UTC),
        onupdate=datetime.now(pytz.UTC),
    )

    def __repr__(self) -> str:
        return "<{0} id={1}>".format(type(self).__name__, self.id)


from .user import User  # noqa
