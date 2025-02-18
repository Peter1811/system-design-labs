from fastapi import FastAPI, Depends


from sqlalchemy.exc import IntegrityError
from app.models import Presentation, engine, Base, SessionLocal
from app.schemas import Pres

from sqlalchemy.orm import Session

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def main():
    return {'a': 'b'}


@app.get('/pres/')
def get_presentations(db: Session = Depends(get_db)):
    return db.query(Presentation).all()


@app.post('/add/')
def add_presentation(pres: Pres, db: Session = Depends(get_db)):
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
    presentations = db.query(Presentation).all()

    return presentations

# @app.post('/register/')
# def register_user()

