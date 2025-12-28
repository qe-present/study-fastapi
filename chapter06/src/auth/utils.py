import logging
import uuid
from datetime import timedelta, datetime
from typing import Tuple, Optional, Dict, Any

import jwt

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from chapter06.src.config import settings

ACCESS_TOKEN_EXPIRE = 3600  # 1 小时，单位秒
# 创建全局实例
ph = PasswordHasher(
    time_cost=3,  # 迭代次数
    memory_cost=65536,  # 64MB 内存
    parallelism=4,  # 并行线程数
    hash_len=32,  # 哈希长度
    salt_len=16,  # 盐长度
)


def hash_password(password: str) -> str:
    """哈希密码（自动处理盐，无长度限制）"""
    return ph.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:

    try:
        ph.verify(hashed_password, plain_password)
        return True
    except VerifyMismatchError:
        return False


def create_access(
        user_data: dict,
        expiry: timedelta = timedelta(seconds=ACCESS_TOKEN_EXPIRE),
        refresh: bool = False,
) -> str:
    """

    :rtype: str
    """
    payload = {
        'user': user_data,
        'exp': datetime.now() + expiry,
        'jti': str(uuid.uuid4()),
        'refresh': refresh
    }
    return jwt.encode(
        payload=payload,
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        return jwt.decode(
            jwt=token,
            key=settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None