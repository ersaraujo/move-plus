from sqlalchemy.orm import Session
from . import models, schemas
from typing import Optional # Importante para tipagem clara

# ===============================================
# FUNÇÕES CRUD PARA PROFISSIONAIS (B2B)
# ===============================================

def get_professional_by_email(db: Session, email: str) -> Optional[models.Professional]:
    return db.query(models.Professional).filter(models.Professional.email == email).first()

def get_professional_by_cref(db: Session, cref_number: str) -> Optional[models.Professional]:
    return db.query(models.Professional).filter(models.Professional.cref_number == cref_number).first()

def get_professional_by_id(db: Session, professional_id: int) -> Optional[models.Professional]:
    return db.query(models.Professional).filter(models.Professional.id == professional_id).first()

def create_professional(db: Session, professional_data: schemas.ProfessionalCreate) -> models.Professional:
    db_professional = models.Professional(
        name=professional_data.name,
        email=professional_data.email,
        cref_number=professional_data.cref_number,
        contact_whatsapp=professional_data.contact_whatsapp,
        is_verified=False
    )
    db.add(db_professional)
    db.commit()
    db.refresh(db_professional)
    return db_professional

# ===============================================

def get_class_by_id(db: Session, class_id: int) -> Optional[models.Class]:
    return db.query(models.Class).filter(models.Class.id == class_id).first()

def get_classes_by_professional(db: Session, professional_id: int) -> list[models.Class]:
    return db.query(models.Class).filter(models.Class.professional_id == professional_id).all()

def create_class(db: Session, class_data: schemas.ClassCreate, professional_id: int) -> models.Class:
    db_class = models.Class(
        name=class_data.name,
        price=class_data.price,
        whatsapp_group_link=class_data.whatsapp_group_link,
        professional_id=professional_id
    )
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class

def get_user_by_whatsapp(db: Session, whatsapp_number: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.whatsapp_number == whatsapp_number).first()

def create_user(db: Session, whatsapp_number: str, class_id: int) -> models.User:
    db_user = models.User(
        whatsapp_number=whatsapp_number,
        class_id=class_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_status(db: Session, user: models.User, new_status: str) -> models.User:
    user.status = new_status
    db.commit()
    db.refresh(user)
    return user

def handle_user_on_inbound(db: Session, whatsapp_number: str, default_class_id: int = 1):
    user = get_user_by_whatsapp(db, whatsapp_number)
    if user:
        print(f"Usuário existente encontrado: {user.whatsapp_number} com status {user.status}")
        return user
    
    print(f"Nenhum usuário encontrado para {whatsapp_number}. Criando novo usuário.")
    return create_user(db=db, whatsapp_number=whatsapp_number, class_id=default_class_id)