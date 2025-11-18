# app/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base

class Professional(Base):
    __tablename__ = "professionals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    cref_number = Column(String, unique=True, index=True, nullable=True)
    contact_whatsapp = Column(String)
    is_verified = Column(Boolean, default=False)

    classes = relationship("Class", back_populates="professional_info")

class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    whatsapp_group_link = Column(String)

    professional_id = Column(Integer, ForeignKey("professionals.id")) 
    professional_info = relationship("Professional", back_populates="classes") 

    users = relationship("User", back_populates="class_info")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    whatsapp_number = Column(String, unique=True, index=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    
    status = Column(String, default="INITIAL") 
    payment_link = Column(String, nullable=True)
    
    class_id = Column(Integer, ForeignKey("classes.id"))

    class_info = relationship("Class", back_populates="users")