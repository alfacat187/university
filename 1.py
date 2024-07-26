import sqlite3
from pathlib import Path

from sqlalchemy import (
    create_engine,
    Table,
    MetaData,
    Column,
    String,
    Integer,
    insert,
    delete,
    select,
)
from sqlalchemy.orm import Session
BASE_DIR = Path(__file__).parent
db_url = f"sqlite:///{BASE_DIR}/my_db_2.db"
#db_url_for_sql = f'{BASE_DIR}/my_db_2.db'

metadata_obj = MetaData()

engine = create_engine(
    db_url,
    echo=True,
)
# user_account = Table(
#     "user_account",
#     metadata_obj,
#     Column("id", Integer, primary_key=True),
#     Column("name", String(50)),
#     Column("fullname", String(50)),
# )
#
#metadata_obj.create_all(engine)
#обращемся уже к прописанным ранее таблицам т.е. не создавали через core или orm
user_account = Table(
    'user_account',
    metadata_obj,
    autoload_with=engine,
)


# with engine.connect() as conn:
#     conn.execute(delete(user_account).where(user_account.c.id == 1))
#     # cursor.execute('DELETE FROM user_account WHERE id == 1')
#     conn.commit()

with engine.connect() as conn:
    stmt = select(user_account.c.fullname).where(user_account.c.name == 'King')
    result = conn.execute(stmt).scalars()
    print(result.all())
