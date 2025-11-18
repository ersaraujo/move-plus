from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/professionals",
    tags=["Professionals"],
)

@router.post("/", response_model=schemas.ProfessionalSchema, status_code=status.HTTP_201_CREATED)
def create_professional(professional: schemas.ProfessionalCreate, db: Session = Depends(get_db)):
    db_prof_email = crud.get_professional_by_email(db, email=professional.email)
    if db_prof_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_prof_cref = crud.get_professional_by_cref(db, cref_number=professional.cref_number)
    if db_prof_cref:
        raise HTTPException(status_code=400, detail="CREF number already registered")
    
    return crud.create_professional(db=db, professional_data=professional)

@router.get("/", response_model=List[schemas.ProfessionalSchema])
def read_professionals(db: Session = Depends(get_db)):
    professionals = db.query(crud.models.Professional).all()
    return professionals