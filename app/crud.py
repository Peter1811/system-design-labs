from sqlalchemy.orm import Session
from typing import Any

from .models import Conference, Presentation, User


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

    
    def get_conference_by_name(self, db: Session, name: str):
        '''
        Получение доклада по названию.
        '''

        conference = db.query(self.model).filter(self.model.name == name).first()
        return conference
    
    
    def delete(self, db: Session, mongo_db: obj_id: int):
        conference_to_delete = self.read(db, obj_id)
        if conference_to_delete:
            presentations = conference_to_delete.presentations
            for presentation in presentations:
                presentation.host_conference = None
        



class UserCRUD(BaseCRUD):

    def __init__(self):
        self.model = User

    
    def get_user_by_login(self, db: Session, login: str):
        '''
        Получение пользователя по логину.
        '''

        user = db.query(self.model).filter(self.model.login == login).first()
        return user
    

    def get_user_by_first_last_name(self, db: Session, first_name: str, last_name: str):
        '''
        Получение пользователей по маске имя-фамилия.
        '''

        users = db.query(self.model).filter(self.first_name == first_name \
                                            & self.model.last_name == last_name).all()
        return users


presCRUD = PresentationCRUD()
confCRUD = ConferenceCRUD()
userCRUD = UserCRUD()
