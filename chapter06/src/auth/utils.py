from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# 创建全局实例
ph = PasswordHasher(
    time_cost=3,        # 迭代次数
    memory_cost=65536,  # 64MB 内存
    parallelism=4,      # 并行线程数
    hash_len=32,        # 哈希长度
    salt_len=16,        # 盐长度
)


def hash_password(password: str) -> str:
    """哈希密码（自动处理盐，无长度限制）"""
    return ph.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    try:
        ph.verify(hashed_password, plain_password)
        # 检查是否需要重新哈希（如参数升级）
        if ph.check_needs_rehash(hashed_password):
            return "rehash_needed"  # 可触发更新
        return True
    except VerifyMismatchError:
        return False