from sqlalchemy import Column, String, Integer, Float, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Region(Base):
    __tablename__ = 'regions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    borrowers = relationship("BorrowerProfile", back_populates="region")

class BorrowerProfile(Base):
    __tablename__ = 'borrower_profiles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    height_cm = Column(Float)
    weight_kg = Column(Float)
    gender = Column(String, nullable=False)
    sport_license = Column(Boolean, default=False)
    education_level = Column(String)
    smoker = Column(Boolean, default=False)
    is_french_citizen = Column(Boolean, default=True)
    estimated_monthly_income = Column(Float)
    marital_status = Column(String)
    credit_history = Column(String)
    personal_risk_level = Column(String)
    account_creation_date = Column(Date)
    credit_score = Column(Float)
    monthly_rent = Column(Float)
    requested_loan_amount = Column(Float, nullable=False)

    # Foreign key + relationship
    region_id = Column(Integer, ForeignKey("regions.id"))
    region = relationship("Region", back_populates="borrowers")
