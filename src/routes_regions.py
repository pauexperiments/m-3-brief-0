
from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
import models, schemas
from database import get_db
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(prefix="/regions", tags=["regions"])


@router.get("/", response_model=List[schemas.RegionRead])
def list_regions(db: Session = Depends(get_db)):
    return db.query(models.Region).all()

@router.get("/{region_id}", response_model=schemas.RegionRead)
def get_region(region_id: int, db: Session = Depends(get_db)):
    region = db.query(models.Region).filter(models.Region.id == region_id).first()
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")
    return region

@router.post("/", response_model=schemas.RegionRead)
def create_region(region: schemas.RegionBase, db: Session = Depends(get_db)):
    existing = db.query(models.Region).filter_by(name=region.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Region already exists")
    db_region = models.Region(name=region.name)
    db.add(db_region)
    db.commit()
    db.refresh(db_region)
    return db_region

@router.delete("/{region_id}", status_code=204)
def delete_region(region_id: int, db: Session = Depends(get_db)):
    region = db.query(models.Region).filter(models.Region.id == region_id).first()
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")
    
    if region.borrowers:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete region: it is assigned to one or more borrowers"
        )
    
    db.delete(region)
    db.commit()
    return None
