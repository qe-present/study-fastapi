from typing import Optional

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException
from fastapi import status
from .utils import decode_token


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(
            self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        creds = await super().__call__(request)
        token = decode_token(creds.credentials)
        if not self.verify_jwt(creds.credentials):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        self.verify_token(token)
        return token

    @staticmethod
    def verify_jwt(jwt_token: str) -> bool:
        payload = decode_token(jwt_token)
        return bool(payload)
    def verify_token(self,token:dict) -> None:
        raise NotImplementedError(
            "Subclasses must implement verify_token method"
        )

class JWTVerifyBearer(JWTBearer):
    def verify_token(self,token:dict) -> None:
        if token and token['refresh']:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Please provide access token")

class JWTRefreshBearer(JWTBearer):
    def verify_token(self,token:dict) -> None:
        if token and not token['refresh']:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Please provide refresh token")