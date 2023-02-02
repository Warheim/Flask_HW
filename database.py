from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, create_engine, func
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import atexit

DSN = 'postgresql://warheim:120290@127.0.0.1:5431/crud'
engine = create_engine(DSN)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class UserModel(Base):
    __tablename__ = 'app_user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)


class AdvertisementModel(Base):
    __tablename__ = 'app_adv'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String)
    creation_date = Column(DateTime, server_default=func.now())
    author = Column(Integer, ForeignKey('app_user.id', ondelete='CASCADE'))
    users = relationship(UserModel, backref='app_adv')


Base.metadata.create_all(bind=engine)
atexit.register(engine.dispose)
