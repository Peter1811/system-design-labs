from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import Any, Union

from app.auth import hash_password, verify_password, create_access_token, decode_access_token
from app.models import Presentation, engine, Base, SessionLocal, User
from app.schemas import PresentationCreate, UserCreate, UserLogin

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/create_user/')
def register(user: UserCreate, 
             db: Session = Depends(get_db)):
    '''
    Регистрация нового пользователя.
    '''

    hashed_password = hash_password(user.password)

    if db.query(User).filter(User.email == user.email).first():
        return {'error': 'Пользователь с такой почтой уже существует'}
    
    new_user = User(email=user.email,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    hashed_password=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.post('/get_token')
def login_for_access_token(form_data: UserLogin = Depends(),
                           db: Session = Depends(get_db)) -> dict[str, str]:
    '''
    Получение токена.
    '''

    user = db.query(User).filter(User.email == form_data.email).first()

    if not user:
        return {'error': 'Такого пользователя нет в базе'}
    
    if not verify_password:
        return {'error': 'Неверный пароль'}
    
    access_token = create_access_token({'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}


@app.post('/add_presentation/')
def add_presentation(pres: PresentationCreate, 
                     db: Session = Depends(get_db)):
    '''
    Создание доклада и добавление в базу данных.
    Если доклад с таким названием уже существует
    в базе данных, выдается сообщение об ошибке.
    '''

    new_pres = Presentation(name=pres.name, description=pres.description)
    db.add(new_pres)

    try:
        db.commit()
        db.refresh(new_pres)
    except IntegrityError:
        return {'error': 'Доклад с таким названием уже существует в базе данных'}

    return new_pres


@app.get('/get_presentations/')
def get_presentations(db: Session = Depends(get_db)):
    '''
    Получение списка всех добавленных докладов.
    '''

    presentations = db.query(Presentation).all()
    if len(presentations) == 0:
        return {'message': 'Докладов на данный момент не добавлено'}

    result = {}
    for presentation in presentations:
        result[presentation.name] = presentation

    return result



@app.get('/get_presentations/')
def get_presentations(db: Session = Depends(get_db)):
    presentations = db.query(Presentation).all()

    return presentations

# @app.post('/register/')
# def register_user()

