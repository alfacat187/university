from typing import List, Optional
from pathlib import Path

from sqlalchemy import (
    create_engine,
    text,
    select,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
    insert,
)
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, relationship

BASE_DIR = Path(__file__).parent
db_url = f"sqlite:///{BASE_DIR}/my_db.db"
engine = create_engine(
    db_url,
    echo=True,
)
# with engine.begin() as connection:
#     connection.execute(text("CREATE TABLE Users (last str, first str)"))
#     connection.execute(
#         text("INSERT INTO Users (last, first) VALUES (:last, :first)"),
#         [
#             {'last': 'Matveev', 'first': 'Alex'},
#             {'last': 'Ivanov', 'first': 'Dima'},
#          ]
#     )
#     connection.commit()
#
# with engine.connect() as connection:
#     result = connection.execute(
#         text("SELECT last, first FROM Users WHERE last == :last"),
#         {'last': 'Ivanov'}
#     )
#     # for row in result.mappings():
#     #     print(row['last'], row['first'])
#     print(result.all())

# with engine.connect() as conn:
#     conn.execute(text('CREATE TABLE Numbers (x int, y int)'))
#     conn.execute(text('INSERT INTO Numbers (x, y) VALUES (:x, :y)'),
#                  [{'x': 1, 'y': 3}])
#     conn.commit()
#     result = conn.execute(text("SELECT * FROM Numbers")).mappings()
#     print(result.all())

# with Session(engine) as session:
#     stmt = text("CREATE TABLE IF NOT EXISTS Numbers (x int, y int)")
#     session.execute(stmt)
#     session.commit()
#
# # with Session(engine) as session:
# #     stmt = text("INSERT INTO Numbers (x, y) VALUES (:x, :y)")
# #     session.execute(
# #         stmt,
# #         [{'x': 1, 'y': 4}, {'x': 5, 'y': 10}]
# #     )
# #     session.commit()
#
# # with Session(engine) as session:
# #     stmt = text("SELECT x, y FROM Numbers WHERE y > :y ORDER BY y")
# #     result = session.execute(stmt, {'y': 5}).all()
# #     print(result)
#
# with Session(engine) as session:
#     stmt = text("UPDATE Numbers SET y=:y WHERE x > :x")
#     session.execute(stmt, {'y': 22, 'x': 2})
#     session.commit()

# with Session(engine) as session:
#     statement = text("CREATE TABLE IF NOT EXISTS Users (first_name str, last_name str, age int)")
#     session.execute(statement)
#     session.commit()
#
# with Session(engine) as session:
#     stmt = text(
#         "INSERT INTO Users (first_name, last_name, age) VALUES (:first_name, :last_name, :age)"
#     )
#     session.execute(stmt, [{'first_name': 'Alex', 'last_name': 'Matveev', 'age': 36},
#                                 {'first_name': 'Mike', 'last_name': 'Gubas', 'age': 44}])
#     session.commit()
#


# user_table = Table(
#     'user_account',
#     metadata_obj,
#     Column('id', Integer, primary_key=True),
#     Column('name', String(30)),
#     Column('fullname', String(50)),
# )
#
# address_table = Table(
#     'address',
#     metadata_obj,
#     Column('id', Integer, primary_key=True),
#     Column('user_id', ForeignKey('user_account.id'), nullable=False),
#     Column('email_address', String(100), nullable=False),
# )


# metadata_obj.drop_all(engine)


# class Base(DeclarativeBase):
#     pass
#
#
# class User(Base):
#     __tablename__ = "user_account"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(30), nullable=False)
#     fullname: Mapped[Optional[str]]
#     addresses: Mapped[List["Address"]] = relationship(back_populates="user")
#
#     def __repr__(self):
#         return f"User={self.id!r} name={self.name!r}"
#
#
# class Address(Base):
#     __tablename__ = "address"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     email_address: Mapped[str]
#     user_id = mapped_column(ForeignKey("user_account.id"), nullable=False)
#     user: Mapped[User] = relationship(back_populates="addresses")
#
#     def __repr__(self) -> str:
#         return f"Address={self.id!r} email_address={self.email_address!r}"
#
#
# Base.metadata.create_all(engine)
#
# user = User(name="Alex", fullname="Matveev")
# print(repr(user))
metadata_obj = MetaData()
user_account = Table('user_account', metadata_obj, autoload_with=engine)
with engine.connect() as conn:
    # stmt = insert(user_account).values()
    conn.execute(insert(user_account),
                 [{'name': 'Sue', 'fullname': 'Scott'}, {'name': 'Debra', 'fullname': 'Matveev'}],)
    conn.commit()
