from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import Any, Union

from app.auth import hash_password, verify_password, create_access_token, decode_access_token
from app.db_config import SessionLocal
from app.models import Conference, Presentation, User
from app.schemas import PresentationCreate, UserCreate, UserLogin

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def main():
    return {'main page': 'main information'}


@app.post('/create_user')
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


@app.post('/login')
def login_for_access_token(form_data: UserLogin = Depends(),
                           db: Session = Depends(get_db)):
    '''
    Получение токена.
    '''

    user = db.query(User).filter(User.login == form_data.login).first()

    if not user:
        return {'error': 'Такого пользователя нет в базе'}
    
    hashed_password = user.hashed_password
    
    if not verify_password(form_data.password, hashed_password):
        return {'error': 'Неверный пароль'}
    
    access_token = create_access_token({'sub': user.login})

    return {'access_token': access_token, 'token_type': 'bearer'}


@app.get('/get_user_by_login')
def get_user_by_login(login: str, db: Session = Depends(get_db)):
    '''
    Поиск пользователя по логину.
    '''

    user = db.query(User).filter(User.email == login).first()

    if not user:
        return {'error': 'Пользователя с таким логином нет в базе данных'}
    
    return user


@app.get('/get_user_by_name')
def get_user_by_name(first_name: str, last_name: str,
                     db: Session = Depends(get_db)):
    '''
    Поиск пользователя по маске имя и фамилия.
    '''

    user = db.query(User).filter(User.first_name == first_name, 
                                 User.last_name == last_name).first()
    
    if not user:
        return {'error': 'Пользователя с такими именем \
                и фамилией нет в базе данных'}
    
    return user


@app.post('/add_presentation')
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


@app.get('/get_presentations')
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


@app.post('/add_pres_to_conf')
def add_presentation_to_conference(presentation_id: int,
                                   conference_id: int,
                                   db: Session = Depends(get_db)):
    '''
    Добавление доклада в конференцию.
    '''

    presentation = db.query(Presentation).get(presentation_id)
    conference = db.query(Conference).get(conference_id)

    if not presentation:
        return {'error': 'Доклада с таким id нет в базе данных'}
    
    if not conference:
        return {'error': 'Конференции с таким id нет в базе данных'}
    
    presentation.conference_id = conference_id

    db.commit()
    db.refresh(presentation)

    return True


@app.get('/test')
def test(a: str):
    return {'a': a}
