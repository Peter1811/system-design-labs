import jwt

from fastapi import FastAPI, Depends, Request, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import Any, Union
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from app.auth import hash_password, verify_password, create_access_token, decode_access_token, get_current_user_login
from app.crud import confCRUD, presCRUD, userCRUD
from app.db_config import SessionLocal
from app.models import Conference, Presentation, User
from app.mongo_config import mongo_presentations
from app.schemas import PresentationCreate, PresentationMongo, UserCreate, UserLogin

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


def check_if_token_is_valid(func):
    def wrapped_func(token):
        decoded_token = decode_access_token(token)
        print(token)
        if decoded_token.get('error'):
            return decoded_token
        
        return func(decoded_token)
    
    return wrapped_func



@app.post('/create_user')
def register(user: UserCreate, 
             db: Session = Depends(get_db)):
    '''
    Регистрация нового пользователя.
    '''

    hashed_password = hash_password(user.password)

    if userCRUD.get_user_by_login(db, user.login):
        return {'error': 'Пользователь с такой почтой уже существует'}
    
    new_user_data = {'login': user.login,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'hashed_password': hashed_password}

    new_user = userCRUD.create(db, **new_user_data)

    return new_user


@app.post('/login')
def login_for_access_token(form_data: UserLogin = Depends(),
                           db: Session = Depends(get_db)):
    '''
    Получение токена.
    '''

    user = userCRUD.get_user_by_login(db, form_data.login)

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

    user = userCRUD.get_user_by_login(db, login)

    if not user:
        return {'error': 'Пользователя с таким логином нет в базе данных'}
    
    return user


@app.get('/get_user_by_name')
def get_user_by_name(first_name: str, last_name: str,
                     db: Session = Depends(get_db)):
    '''
    Поиск пользователя по маске имя и фамилия.
    '''

    user = userCRUD.get_user_by_first_last_name(db, first_name, last_name)
    
    if not user:
        return {'error': 'Пользователей с такими именем \
                и фамилией нет в базе данных'}
    
    return user


@app.post('/add_presentation')
@check_if_token_is_valid
def add_presentation(pres: PresentationCreate, 
                     db: Session = Depends(get_db)):
    '''
    Создание доклада и добавление в базу данных.
    Если доклад с таким названием уже существует
    в базе данных, выдается сообщение об ошибке.
    '''

    new_pres_data = {'name': pres.name,
                     'description': pres.description}
    
    try:
        new_pres = presCRUD.create(db, **new_pres_data)
    except IntegrityError:
        db.rollback()
        return {'error': 'Доклад с таким названием уже существует в базе данных'}

    return new_pres or None


@app.get('/get_presentations')
def get_presentations(db: Session = Depends(get_db)):
    '''
    Получение списка всех добавленных докладов.
    '''

    presentations = db.query(Presentation).all()
    if len(presentations) == 0:
        return {'message': 'Докладов на данный момент не добавлено'}

    return presentations


@app.post('/add_pres_to_conf')
@check_if_token_is_valid
def add_presentation_to_conference(presentation_name: int,
                                   conference_name: int,
                                   db: Session = Depends(get_db)):
    '''
    Добавление доклада в конференцию.
    '''

    presentation = presCRUD.get_presentation_by_name(db, presentation_name)
    conference = confCRUD.get_conference_by_name(db, conference_name)

    if not presentation:
        return {'error': 'Доклада с таким id нет в базе данных'}
    
    if not conference:
        return {'error': 'Конференции с таким id нет в базе данных'}
    
    presentation.conference_id = conference.id

    db.commit()
    db.refresh(presentation)

    return True


@app.post('/add-presentation-with-text')
def add_presentation_with_text(presentation_for_mongo: PresentationMongo = Body(...)):
    new_pres = {'res': None}
    if not mongo_presentations.find_one({'name': presentation_for_mongo.name}):
        new_pres = {
            'name': presentation_for_mongo.name,
            'pres_text': presentation_for_mongo.text
        }
        mongo_presentations.insert_one(new_pres)
        return new_pres

    return new_pres


@app.get('/get-presentation-with-text')
def get_presentation_With_text(name: str):
    pres = mongo_presentations.find_one({'name': name})
    if pres:
        return {k: pres[k] for k in pres if k != '_id'}
    
    return pres
    

@app.get('/test-mongo')
def test_mongo():
    pres = mongo_presentations.find_one({'name': 'Machine Learning for Big Data: Tools and Techniques'})
    print(type(pres))
    return {'pres': {k: pres[k] for k in pres if k != '_id'}}


@app.get('/protected')
@check_if_token_is_valid
def test(token: str):
    return {'user': token}
