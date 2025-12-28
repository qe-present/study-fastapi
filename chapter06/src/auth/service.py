from sqlmodel import select

from sqlmodel.ext.asyncio.session import AsyncSession
from .models import User
from .schemas import User as UserSchema
from .utils import hash_password


class UserService:
    @staticmethod
    async def get_user_by_email(email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        results = await session.exec(statement)
        return results.one_or_none()

    async def user_exists(self, email: str, session: AsyncSession) -> bool:
        user = await self.get_user_by_email(email, session)
        return user is not None

    async def create_user(self, user_data: UserSchema, session: AsyncSession):
        # 变成字典
        user_dict = user_data.model_dump()
        new_user = User(**user_dict)
        new_user.password_hash = hash_password(user_dict['password'])
        session.add(new_user)
        await session.commit()
        return new_user
