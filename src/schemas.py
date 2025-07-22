from pydantic import BaseModel
from datetime import date
from typing import Optional

class RegionBase(BaseModel):
    name: str

class RegionRead(RegionBase):
    id: int
    class Config:
        orm_mode = True

class BorrowerProfileBase(BaseModel):
    first_name: str
    last_name: str
    age: int
    height_cm: Optional[float]
    weight_kg: Optional[float]
    gender: str
    sport_license: Optional[bool] = False
    education_level: Optional[str]
    smoker: Optional[bool] = False
    is_french_citizen: Optional[bool] = True
    estimated_monthly_income: Optional[float]
    marital_status: Optional[str]
    credit_history: Optional[str]
    personal_risk_level: Optional[str]
    account_creation_date: date
    credit_score: Optional[float]
    monthly_rent: Optional[float]
    requested_loan_amount: float
    region_id: Optional[int]  # Use foreign key here

class BorrowerProfileCreate(BorrowerProfileBase):
    pass

class BorrowerProfileRead(BorrowerProfileBase):
    id: int
    region: Optional[RegionRead]

    class Config:
        orm_mode = True
