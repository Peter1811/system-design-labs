from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, TIMESTAMP, func
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


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
    is_superuser = Column(Boolean, default=False)
    login = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
