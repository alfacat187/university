from pydantic import BaseModel
# from pathlib import Path
#
# from sqlalchemy import String, Integer, create_engine, insert, select
# from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, Session
#
# BASE_DIR = Path(__file__).parent
# db_url = f'sqlite:///{BASE_DIR}/my_db_2.db'
# engine = create_engine(db_url, echo=True)
#
#
# class Base(DeclarativeBase):
#     pass
#
#
# class User(Base):
#     __tablename__ = 'user_account_2'
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str]
#     fullname: Mapped[str] = mapped_column(String(100), nullable=False)
#
#
# Base.metadata.create_all(engine)
# with Session(engine) as session:
#     stmt = select(User.id).where(User.name == 'alex')
#     result = session.execute(stmt).scalars()
#     # result.mappings()
#     print(result.all())


class TunedModel:
    class Config:
        """Config"""
        color = 'red'


p = TunedModel()
var = p.Config
print(var.__annotations__)
print(var)
print(dir(p))