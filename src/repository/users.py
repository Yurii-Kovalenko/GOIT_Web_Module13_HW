from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel
from src.conf.config import settings

from redis import Redis
from pickle import dumps, loads

redis_db = Redis(host=settings.redis_host, port=settings.redis_port, db=0)


async def get_user_by_email_from_db(email: str, db: Session) -> User:
    return db.query(User).filter(User.email == email).first()


async def get_user_by_email(email: str, db: Session) -> User:
    user_dump = redis_db.get(email)
    if user_dump is None:
        user = db.query(User).filter(User.email == email).first()
        redis_db.set(email, dumps(user))
        return user
    return loads(user_dump)


async def create_user(body: UserModel, db: Session) -> User:
    new_user = User(**body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    user_dump = redis_db.get(new_user.email)
    if user_dump:
        redis_db.delete(new_user.email)
    return new_user


async def update_token(cash_user: User, token: str | None, db: Session) -> None:
    user = await get_user_by_email_from_db(cash_user.email, db)
    user.refresh_token = token
    db.commit()
    user_dump = redis_db.get(user.email)
    if user_dump:
        redis_db.delete(user.email)


async def confirmed_email(email: str, db: Session) -> None:
    user = await get_user_by_email_from_db(email, db)
    user.confirmed = True
    db.commit()
    user_dump = redis_db.get(email)
    if user_dump:
        redis_db.delete(email)


async def update_password(cash_user: User, password: str, db: Session) -> None:
    user = await get_user_by_email_from_db(cash_user.email, db)
    user.password = password
    db.commit()
    user_dump = redis_db.get(user.email)
    if user_dump:
        redis_db.delete(user.email)


async def update_avatar(email, url: str, db: Session) -> User:
    user = await get_user_by_email_from_db(email, db)
    user.avatar = url
    db.commit()
    user_dump = redis_db.get(email)
    if user_dump:
        redis_db.delete(email)
    return user
