import jwt

from fastapi import FastAPI, Depends, Request, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import Any, Union
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure

from app.auth import hash_password, verify_password, create_access_token, decode_access_token, get_current_user_login
from app.conf_post_router import router
from app.crud import confCRUD, presCRUD, userCRUD
from app.db_config import get_db
from app.models import Conference, Presentation, User
from app.mongo_config import get_mongo
from app.redis_config import get_redis
from app.schemas import PresentationCreate, PresentationMongo, UserCreate, UserLogin
from app.utils import check_if_token_is_valid

app = FastAPI()

app.include_router(router, prefix='/post_kafka', tags=['conference'])


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
    
    return {'first_name': user.first_name,
            'last_name': user.last_name,
            'login': user.login}


@app.get('/get_user_by_name')
def get_user_by_name(first_name: str, last_name: str,
                     db: Session = Depends(get_db)):
    '''
    Поиск пользователя по маске имя и фамилия.
    '''

    users = userCRUD.get_users_by_first_last_name(db, first_name, last_name)
    
    if not users:
        return {'error': 'Пользователей с такими именем и фамилией нет в базе данных'}
    
    return [{'first_name': user.first_name,
            'last_name': user.last_name,
            'login': user.login} for user in users]


@app.post('/add_presentation')
@check_if_token_is_valid
def add_presentation(token: str,
                    pres: PresentationCreate, 
                    mongo_presentations: Collection = Depends(get_mongo),
                    db: Session = Depends(get_db)):
    '''
    Создание доклада и добавление в базу данных.
    Если доклад с таким названием уже существует
    в базе данных, выдается сообщение об ошибке.
    '''

    new_pres_data = {'name': pres.name,
                     'description': pres.description}
    
    new_pres_data_for_mongo = {'name': pres.name,
                               'text': pres.text}
    
    try:
        new_pres = presCRUD.create(db, **new_pres_data)
    except IntegrityError:
        db.rollback()
        return {'error': 'Доклад с таким названием уже существует в базе данных'}
    
    mongo_presentations.insert_one(new_pres_data_for_mongo)

    return {'added': new_pres}


@app.get('/get_presentations')
def get_presentations(db: Session = Depends(get_db), 
                      mongo_presentations: Collection = Depends(get_mongo)):
    '''
    Получение списка всех добавленных докладов.
    '''

    presentations = db.query(Presentation).all()
    if len(presentations) == 0:
        return {'message': 'Докладов на данный момент не добавлено'}
    
    all_presentations = []
    for pres in presentations:
        pres_with_text = mongo_presentations.find_one({'name': pres.name})
        new_pres = {}
        new_pres['name'] = pres.name
        new_pres['description'] = pres.description
        if pres_with_text:
            new_pres['text'] = pres_with_text['pres_text']
        if pres.conference_id:
            new_pres['conference'] = confCRUD.read(db, pres.conference_id)

        if new_pres:
            all_presentations.append(new_pres)



    return all_presentations


@app.get('/get_conferences')
def get_conferences(db: Session = Depends(get_db)):
    '''
    Получение списка актуальных конференций (с докладами,
    привязанными к конференции).
    '''

    conferences = db.query(Conference).all()

    return [{'name': conference.name,
             'description': conference.description,
             'presentations': conference.presentations} for conference in conferences]


@app.post('/add_pres_to_conf')
@check_if_token_is_valid
def add_presentation_to_conference(token: str,
                                   presentation_name: str,
                                   conference_name: str,
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


# @app.delete('/del_conf')
# def delete_conf(db: Session = Depends(get_db)):
#     confCRUD.delete(db, 4)


# @app.get('/test_get')
# def read_pres(db: Session = Depends(get_db)):
#     res = presCRUD.get_presentation_by_name(db, 'Asynchronous Programming in Python: A Deep Dive')
#     print(res.host_conference)
#     return res


@app.get('/redis_test')
def test_redis(db: Session = Depends(get_db), 
               r = Depends(get_redis)):
    res = confCRUD.get_conference_by_name(db, 'DockerCon')
    return res