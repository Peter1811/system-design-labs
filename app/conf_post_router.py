from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .crud import confCRUD
from .db_config import get_db
from .schemas import ConferenceCreate
from .utils import check_if_token_is_valid

router = APIRouter()


@router.post('/add_conference')
@check_if_token_is_valid
def add_conference(token: str,
                    conf: ConferenceCreate, 
                    db: Session = Depends(get_db)):
    '''
    Создание конференции и добавление в базу данных.
    Если конференция с таким названием уже существует
    в базе данных, выдается сообщение об ошибке.
    '''

    new_pres_data = {'name': conf.name,
                     'description': conf.description}
    try:
        new_conf = confCRUD.create(db, **new_pres_data)
    except IntegrityError:
        db.rollback()
        return {'error': 'Конференция с таким названием уже существует в базе данных'}

    return {'added': new_conf}