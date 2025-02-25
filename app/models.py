from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import DeclarativeBase, declarative_base, sessionmaker, relationship

class Base(DeclarativeBase):
    pass


DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = '1811'

DATABASE_URL = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class Presentation(Base):
    __tablename__ = 'presentations'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(Text)
    conference_id = Column(Integer, ForeignKey('conferences.id'))

    host_conference = relationship('Conference', back_populates='presentations')


class Conference(Base):
    __tablename__ = 'conferences'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    presentations = relationship('Presentation', back_populates='host_conference')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
