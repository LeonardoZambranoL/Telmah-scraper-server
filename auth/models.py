from cryptography.fernet import Fernet
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from authdbAttributes import db_encryption_key
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True)
    firstname = Column("firstname", String)
    lastname = Column("lastname", String)
    password_hash = Column(String, nullable=False)
    rucs = relationship('Ruc', back_populates='user')

    def __init__(self, email, firstname, lastname, password_hash):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password_hash = password_hash

    def __repr__(self):
        return f"id: {self.id} email: {self.email} nombre: {self.firstname} lastname: {self.lastname} rucs: {self.rucs}"


class Ruc(Base):
    __tablename__ = "rucs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ruc = Column("ruc", String)
    user_email = Column(String, ForeignKey('users.id'))
    user = relationship('User', back_populates='rucs')

    def __init__(self, ruc, user):
        cipher_suite = Fernet(db_encryption_key)
        self.ruc = cipher_suite.encrypt(ruc.encode()).decode("utf8")
        self.user = user

    def __repr__(self):
        return f"ruc: {self.ruc} user: {self.user.email}"
