import json

from pymongo.collection import Collection
from sqlalchemy import and_
from sqlalchemy.orm import Session
from typing import Any

from .models import Conference, Presentation, User
from .redis_config import get_redis


class BaseCRUD:
    '''
    Базовый класс для переопределения операций
    CRUD с объектами (поиск выполняется только 
    для индекса).
    '''

    def __init__(self):
        self.model = None


    def create(self, db: Session, **kwargs):
        '''
        Создание объекта
        '''

        new_obj = self.model(**kwargs)
        db.add(new_obj)
        db.commit()

        return new_obj


    def read(self, db: Session, obj_id: int):
        '''
        Получение объекта
        '''

        obj = db.query(self.model).get(obj_id)
        return obj


    def update(self, db: Session, obj_id: int, **kwargs):
        '''
        Обновление объекта
        '''

        obj = self.read(db, obj_id)
        if obj:
            updated_obj = self.model(**kwargs)
            db.add(updated_obj)
            db.commit()

        return obj


    def delete(self, db: Session, obj_id: int):
        '''
        Удаление объекта
        '''

        obj = self.read(db, obj_id)
        if obj:
            db.delete(obj)
            db.commit()

        return obj    


class PresentationCRUD(BaseCRUD):

    def __init__(self):
        self.model = Presentation


    def get_presentation_by_name(self, db: Session, name: str):
        '''
        Получение доклада по названию.
        '''

        presentation = db.query(self.model).filter(self.model.name == name).first()
        return presentation


class ConferenceCRUD(BaseCRUD):

    def __init__(self):
        self.model = Conference


    def read(self, db, obj_id):
        redis_connection = next(get_redis())
        if redis_connection:
            redis_key = f'conference:name:{obj_id}'
            redis_cached_data = redis_connection.get(redis_key)
            if redis_cached_data:
                return json.loads(redis_cached_data)

            conference = db.query(self.model).get(obj_id)
            if conference:
                conference_dict = conference.__dict__
                redis_connection.set(redis_key, json.dumps({k: conference_dict[k] 
                                                            for k in conference_dict 
                                                            if k != '_sa_instance_state'}), 3600)
        return conference
        

    
    def get_conference_by_name(self, db: Session, name: str):
        '''
        Получение доклада по названию.
        Сначала проверяется, есть ли значение в кэше redis,
        потом 
        '''
        redis_connection = next(get_redis())
        if redis_connection:
            redis_key = f'conference:name:{name}'
            redis_cached_data = redis_connection.get(redis_key)
            if redis_cached_data:
                return json.loads(redis_cached_data)

            conference = db.query(self.model).filter(self.model.name == name).first()
            if conference:
                conference_dict = conference.__dict__
                redis_connection.set(redis_key, json.dumps({k: conference_dict[k] 
                                                            for k in conference_dict 
                                                            if k != '_sa_instance_state'}), 3600)
        return conference
    
    
    def delete(self, db: Session, obj_id: int):
        '''
        Удаление конференции: при удалении обнуляются ссылки
        на данную конференцию у всех докладов, добавленных в
        эту конференцию.
        '''

        conference_to_delete = self.read(db, obj_id)
        if conference_to_delete:
            presentations = conference_to_delete.presentations
            for presentation in presentations:
                curr_pres = presCRUD.read(db, presentation.id)
                curr_pres.conference_id = None

                db.add(curr_pres)
            db.commit()


class UserCRUD(BaseCRUD):

    def __init__(self):
        self.model = User

    
    def get_user_by_login(self, db: Session, login: str):
        '''
        Получение пользователя по логину.
        '''

        user = db.query(self.model).filter(self.model.login == login).first()
        return user
    

    def get_users_by_first_last_name(self, db: Session, first_name: str, last_name: str):
        '''
        Получение пользователей по маске имя-фамилия.
        '''

        users = db.query(self.model).filter(and_(self.model.first_name == first_name, self.model.last_name == last_name)).all()
        return users


presCRUD = PresentationCRUD()
confCRUD = ConferenceCRUD()
userCRUD = UserCRUD()
