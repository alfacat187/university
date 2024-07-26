import uuid
import re

from sqlalchemy import String, Boolean
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from pydantic import BaseModel, EmailStr, field_validator
from fastapi import FastAPI, HTTPException, APIRouter

from config import settings


engine = create_async_engine(
    settings.db_url,
    echo=True
)
async_session = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
    autocommit=False
)
# @declared_attr.directive - действует как проперти


class Base(DeclarativeBase):
    pass
    # __abstract__ = True  # это атрибут для sqlalchemy не создается в бд
    #
    # @declared_attr.directive
    # def __tablename__(cls) -> str:
    #     return f'{cls.__name__.lower()}s'

    # id: Mapped[str] = mapped_column(primary_key=True)


class User(Base):
    __tablename__ = 'users'
    user_id: Mapped[int] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)





class UserDAL:
    """
    Data Access Layer for operating user info.
    """
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, name: str, surname: str, email: str) -> User:
        new_user = User(
            name=name,
            surname=surname,
            email=email,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()

        return new_user


LETTER_MATCH_PATTERN = re.compile(r'[а-яА-Яa-zA-Z\-]+$')


class TunedModel(BaseModel):
    class Config:
        orm_mod = True


class ShowUser(TunedModel):
    user_id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    is_active: bool


class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr

    @field_validator('name')
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail='Name contains only letters!',
            )
        return value

    @field_validator('surname')
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail='Surname contains only letters!'
            )
        return value


app = FastAPI(title='University')

user_router = APIRouter(prefix='/user', tags=['User'])

async def _create_new_user(body: UserCreate) -> ShowUser:
    async with async_session() as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                name=body.name,
                surname=body.surname,
                email=body.email,
            )
            return ShowUser(
                user_id=user.user_id,
                name=user.name,
                surname=user.surname,
                email=user.email,
                is_active=user.is_active,
            )


@app.post('/', response_model=ShowUser)
async def create_user(body: UserCreate) -> ShowUser:
    return await _create_new_user(body)


main_api_router = APIRouter()
main_api_router.include_router(user_router)
app.include_router(main_api_router)


if __name__ == '__main__':
    # Base.metadata.create_all(engine)
    import uvicorn
    uvicorn.run('main:app', reload=True, port=9000)