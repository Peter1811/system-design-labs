from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .crud import confCRUD
from .db_config import get_db
from .kafka_config import send_data_to_kafka
from .schemas import ConferenceCreate
from .utils import check_if_token_is_valid

router = APIRouter()


@check_if_token_is_valid
@router.post('/add_conference')
def add_conference(conf: ConferenceCreate, 
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
    
    message = f'{new_pres_data["name"]}=>{new_pres_data["description"]}'
    send_data_to_kafka('conference_topic', message)

    return {'added': new_conf}