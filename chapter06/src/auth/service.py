from datetime import timedelta

from fastapi import HTTPException
from sqlmodel import select

from sqlmodel.ext.asyncio.session import AsyncSession

from fastapi.responses import JSONResponse
from fastapi import status
from .models import User
from .schemas import User as UserSchema, Login
from .utils import hash_password, create_access, decode_token, verify_password


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

    async def login_user(self, user_data: Login, session: AsyncSession):
        user = await self.get_user_by_email(user_data.email, session)
        is_verify = verify_password(user_data.password, user.password_hash)
        if not is_verify:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid credentials")
        access_token = create_access({"email": user.email, 'uid': str(user.uid)})
        refresh_token = create_access(
            {"email": user.email, 'uid': str(user.uid)},
            expiry=timedelta(days=1),
            refresh=True
        )
        return JSONResponse(
            content={
                "message": "Login successful",
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        )
