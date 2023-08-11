from sqlalchemy import create_engine, String, ForeignKey, BigInteger, DateTime, Boolean

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import as_declarative, Mapped, mapped_column, Session, declared_attr

from sqlalchemy.sql.functions import current_timestamp

from db.base import BaseModel


class User(BaseModel):
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    fullname: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    bonus_points: Mapped[int] = mapped_column(nullable=True, default=0)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_owner: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    def __repr__(self) -> str:
        return f'''time:{self.timestamp}; id: {self.id}; user_id: {self.user_id}; fullname: {self.fullname};
            phone_num: {self.phone_number}; email: {self.email}; bonus_points: {self.bonus_points}\n'''
    
    def __eq__(self, __o: object) -> bool:
        if __o._sa_class_manager.class_ is not User:
            return NotImplemented
        return (
            self.user_id == __o.user_id
            and self.phone_number == __o.phone_number
            and self.email == __o.email
        )

    def __ne__(self, __o: object) -> bool:
        if __o._sa_class_manager.class_ is not User:
            return NotImplemented
        return not (
            self.user_id == __o.user_id
            and self.phone_number == __o.phone_number
            and self.email == __o.email
        )
