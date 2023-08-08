from sqlalchemy import create_engine, String, ForeignKey, BigInteger, DateTime, select

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import as_declarative, Mapped, mapped_column, Session, declared_attr

from sqlalchemy.sql.functions import current_timestamp


@as_declarative()
class BaseModel:
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)

    __allow_unmapped__ = False

    @classmethod
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class User(BaseModel):
    timestamp: Mapped[DateTime] = mapped_column(DateTime, nullable=False, server_default=current_timestamp(), onupdate=current_timestamp())
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    fullname: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    bonus_points: Mapped[int] = mapped_column()

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


class Database():

    def __init__(self, db_path: str = None):
        if not db_path:
            db_path = ':memory:'
        
        self.engine = create_engine(f'sqlite:///{db_path}', echo=False)
        BaseModel.metadata.create_all(bind=self.engine)
        self.session = Session(bind=self.engine)
        self.session.begin()
    
    def __del__(self):
        self.session.close()

    def add_user(self, user: User) -> None:
        self.session.add(user)
        self.session.commit()

    def get_all_users(self):
        result = self.session.query(User).all()
        return result

    def get_user_by_phone_number(self, phone_number: str) -> User:
        result = self.session.query(User).filter(User.phone_number == phone_number).first()
        return result

    def add_bonus_points(self, bonus_points_to_add: int, user: User):
        result = self.session.query(User).filter(User == user).update({User.bonus_points: User.bonus_points + bonus_points_to_add})
        self.session.commit()
        return result

    def delete_all(self):
        self.session.query(User).filter(User.id >= 1).delete()
        self.session.commit()

    def delete_user(self, user: User):
        self.session.query(User).filter(User == user).delete()
        self.session.commit()
