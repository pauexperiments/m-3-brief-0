
from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
import models, schemas
from database import get_db
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(prefix="/borrowers", tags=["borrowers"])


@router.post("/", response_model=schemas.BorrowerProfileRead)
def create_borrower(profile: schemas.BorrowerProfileCreate, db: Session = Depends(get_db)):
    db_profile = models.BorrowerProfile(**profile.dict())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.get("/", response_model=List[schemas.BorrowerProfileRead])
def list_borrowers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.BorrowerProfile).offset(skip).limit(limit).all()

@router.get("/{borrower_id}", response_model=schemas.BorrowerProfileRead)
def get_borrower(borrower_id: int, db: Session = Depends(get_db)):
    profile = db.query(models.BorrowerProfile).filter(models.BorrowerProfile.id == borrower_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Borrower not found")
    return profile

@router.delete("/{borrower_id}", status_code=204)
def delete_borrower(
    borrower_id: int,
    db: Session = Depends(get_db)
):
    profile = db.query(models.BorrowerProfile).filter(models.BorrowerProfile.id == borrower_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Borrower not found")

    db.delete(profile)
    db.commit()
    return None