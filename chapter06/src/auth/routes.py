from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession

from .schemas import User, Register, Login
from .service import UserService
from ..db.main import get_session
from .dependencies import JWTVerifyBearer,JWTRefreshBearer

router = APIRouter(prefix='/auth', tags=['auth'])
service = UserService()
bearer = JWTVerifyBearer()


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
async def login(user: Login,
                session: AsyncSession = Depends(get_session)
                ):
    ok=await service.user_exists(user.email, session)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Not Found')
    return await service.login_user(user, session)
@router.get('/refresh')
async def refresh(token=Depends(JWTRefreshBearer())):
    if datetime.fromtimestamp(token['exp']) > datetime.now():
        return await service.refresh_token(token['user'])
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid token')
@router.get('/test')
async def test(user_detail=Depends(bearer)):
    pass