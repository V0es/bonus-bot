from sqlalchemy import DateTime
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.orm import as_declarative, mapped_column, Mapped, declared_attr


@as_declarative()
class BaseModel:
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    timestamp: Mapped[DateTime] = mapped_column(DateTime, nullable=False, server_default=current_timestamp(), onupdate=current_timestamp())

    __allow_unmapped__ = False

    @classmethod
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
