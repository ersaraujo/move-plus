from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/classes",
    tags=["Classes"],
)

@router.post("/", response_model=schemas.ClassSchema, status_code=status.HTTP_201_CREATED)
def create_class_for_professional(class_data: schemas.ClassCreate, professional_id: int, db: Session = Depends(get_db)):
    professional = crud.get_professional_by_id(db, professional_id=professional_id)
    if not professional:
        raise HTTPException(status_code=404, detail="Professional not found")
    
    return crud.create_class(db=db, class_data=class_data, professional_id=professional_id)

@router.get("/", response_model=List[schemas.ClassSchema])
def read_classes(db: Session = Depends(get_db)):
    classes = db.query(crud.models.Class).all()
    return classes