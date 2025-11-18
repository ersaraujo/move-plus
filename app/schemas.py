from pydantic import BaseModel
from typing import List, Optional

class ProfessionalCreate(BaseModel):
    name: str
    email: str
    cref_number: str
    contact_whatsapp: str

class ProfessionalSchema(BaseModel):
    id: int
    name: str
    email: str
    is_verified: bool
    
    classes: List['ClassSchema'] = [] 

    class Config:
        orm_mode = True

class ClassCreate(BaseModel):
    name: str
    price: float
    whatsapp_group_link: str

class ClassSchema(ClassCreate):
    id: int
    professional_id: int
    
    class Config:
        orm_mode = True

class UserSchema(BaseModel):
    id: int
    name: Optional[str] = None
    whatsapp_number: str
    status: str
    class_id: int
    
    class Config:
        orm_mode = True