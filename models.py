import os
from atexit import register

from sqlalchemy import Column, DateTime, Integer, String, create_engine, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

PG_USER = os.getenv('PG_USER', 'postgres')
PG_PASSWORD = os.getenv('PG_PASSWORD', 'postgres')
PG_DB = os.getenv('PG_DB', 'app')
PG_HOST = os.getenv('PG_HOST', '127.0.0.1')
PG_PORT = os.getenv('PG_PORT', 5431)
PG_DSN = f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}'
engine = create_engine(PG_DSN)

register(engine.dispose)

Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)


class User(Base):
    __tablename__ = 'app_users'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    creation_time = Column(DateTime, server_default=func.now())

    ads = relationship('Advertisement', back_populates='owner', cascade='all, delete')


class Advertisement(Base):
    __tablename__ = 'advertisements'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    creation_time = Column(DateTime, server_default=func.now())
    owner_id = Column(Integer, ForeignKey('app_users.id'))

    owner = relationship('User', back_populates='advertisements')


Base.metadata.create_all()
