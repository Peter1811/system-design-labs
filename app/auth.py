import jwt
import os

from datetime import datetime, timedelta
from dotenv import load_dotenv
from passlib.context import CryptContext
from typing import Any

ACCESS_TOKEN_EXPIRE_MINUTES = 30

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str) -> str:
    '''
    Вычисление хэша пароля.
    '''

    return pwd_context.hash(password)


def verify_password(plain_password: str, hash_password: str) -> bool:
    '''
    Функция выполняет проверку соответствия введенного пароля 
    и хэшированного пароля из базы данных.

    :param plain_password: пароль, полученный из формы ввода;
    :param hash_password: хэшированный пароль из базы данных.
    '''

    return pwd_context.verify(plain_password, hash_password)


def create_access_token(data: dict) -> str:
    '''
    Функция создает токен JWT для дальнейшей
    аутентификации пользователя.

    :param data: словарь с данными (имя пользователя).
    '''

    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    '''
    Функция выполняет декодирование токена на основании
    секретного ключа.

    :param token: токен в виде строки.
    '''

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM, ])
        return payload
    
    except jwt.ExpiredSignatureError:
        return {'error': 'Токен просрочен'}
    
    except jwt.PyJWTError:
        return {'error': 'Токен не является валидным'}
    

def get_current_user_login(token: str):
    payload = decode_access_token(token)
    if payload.get('sub'):
        return payload['sub']
