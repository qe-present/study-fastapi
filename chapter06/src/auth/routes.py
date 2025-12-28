from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession

from .schemas import User, Register
from .service import UserService
from ..db.main import get_session

router = APIRouter(prefix='/auth', tags=['auth'])
service = UserService()


@router.post(
    '/register',
    response_model=Register,
    status_code=status.HTTP_201_CREATED,
)
async def register(
        user: User,
        session: AsyncSession = Depends(get_session)
):
    ok = await service.user_exists(user.email, session)
    if ok:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User Exists')
    new_user = await service.create_user(user, session)
    return new_user


@router.post(
    '/login',
    status_code=status.HTTP_200_OK
)
async def login():
    return {"message": "Login successful"}