from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), index=True)
    last_name = Column(String(50), index=True)
    email = Column(String(50), unique=True, index=True)
    phone_number = Column(String(15), nullable=True)
    birthday = Column(Date, nullable=False)
    additional_data = Column(String(250), nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(Date, default=func.now(), nullable=True)
    updated_at = Column(Date, default=func.now(), onupdate=func.mow(), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    user = relationship("User", backref="contacts", lazy="joined")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True, index=True)
    email = Column(String(50), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False, index=True)
    avatar = Column(String(255), nullable=True, index=True)
    refresh_token = Column(String(255), nullable=True)
    created_at = Column(Date, default=func.now())
    updated_at = Column(Date, default=func.now(), onupdate=func.mow())