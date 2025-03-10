from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, TIMESTAMP, Index
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Presentation(Base):
    __tablename__ = 'presentations'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    conference_id = Column(Integer, ForeignKey('conferences.id'))

    host_conference = relationship('Conference', back_populates='presentations')


class Conference(Base):
    __tablename__ = 'conferences'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    description = Column(String)

    presentations = relationship('Presentation', back_populates='host_conference')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    is_superuser = Column(Boolean, default=False)
    login = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)

    __table_args__ = (
        Index('ix_users_first_name_last_email', 'first_name', 'last_name'),
    )
