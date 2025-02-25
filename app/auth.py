from jwt.jwt import JWT

from datetime import datetime, timedelta
from passlib.context import CryptContext
from typing import Any

SECRET_KEY = 'my_secret_key'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str) -> str:
    '''
    Вычисление хэша пароля.
    '''

    return pwd_context.hash(password)


def verify_password(plain_password: str, hash_password: str) -> bool:
    return pwd_context.verify(plain_password, hash_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    jwt = JWT()
    return jwt.encode(to_encode, SECRET_KEY, alg=ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any] | None:
    jwt = JWT()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    
    except jwt.ExpiredSignatureError:
        return None
    
    except jwt.PyJWTError:
        return None
