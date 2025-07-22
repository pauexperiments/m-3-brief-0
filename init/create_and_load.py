import sys
import os
import pandas as pd
from sqlalchemy.orm import Session
from datetime import datetime


CURRENT_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..', 'src'))
print(f"Current directory: {CURRENT_DIR}")
print(f"Source directory: {SRC_DIR}")

# add src directory to sys.path
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)


from database import SessionLocal, db_create
import models


def load_data(csv_path: str):

    model_cvs_mapping = {
        "first_name": "prenom",
        "last_name": "nom",
        "age": "age",
        "height_cm": "taille",
        "weight_kg": "poids",
        "gender": "sexe",
        "sport_license": "sport_licence",
        "education_level": "niveau_etude",
        "region": "region",
        "smoker": "smoker",
        "is_french_citizen": "nationalité_francaise",
        "estimated_monthly_income": "revenu_estime_mois",
        "marital_status": "situation_familiale",
        "credit_history": "historique_credits",
        "personal_risk_level": "risque_personnel",
        "account_creation_date": "date_creation_compte",
        "credit_score": "score_credit",
        "monthly_rent": "loyer_mensuel",
        "requested_loan_amount": "montant_pret"
    }



    df = pd.read_csv(csv_path)
    db: Session = SessionLocal()

    try:
        for _, row in df.iterrows():
            # print(f"Importing borrower: {row[model_cvs_mapping['first_name']]} {row[model_cvs_mapping['last_name']]}")
            # 1. Get or create region
            region_name = row[model_cvs_mapping["region"]]
            region = db.query(models.Region).filter_by(name=region_name).first()
            if not region:
                print(f"Creating region: {region_name}")
                region = models.Region(name=region_name)
                db.add(region)
                db.commit()
                db.refresh(region)

            # 2. Create BorrowerProfile
            borrower = models.BorrowerProfile(
                first_name=row[model_cvs_mapping["first_name"]],
                last_name=row[model_cvs_mapping["last_name"]],
                age=int(row[model_cvs_mapping["age"]]),
                height_cm=float(row[model_cvs_mapping["height_cm"]]) if not pd.isna(row[model_cvs_mapping["height_cm"]]) else None,
                weight_kg=float(row[model_cvs_mapping["weight_kg"]]) if not pd.isna(row[model_cvs_mapping["weight_kg"]]) else None,
                gender=row[model_cvs_mapping["gender"]],
                sport_license=bool(row[model_cvs_mapping["sport_license"]]),
                education_level=row.get(model_cvs_mapping["education_level"]),
                smoker=bool(row[model_cvs_mapping["smoker"]]),
                is_french_citizen=bool(row[model_cvs_mapping["is_french_citizen"]]),
                estimated_monthly_income=float(row[model_cvs_mapping["estimated_monthly_income"]]) if not pd.isna(row[model_cvs_mapping["estimated_monthly_income"]]) else None,
                marital_status=row.get(model_cvs_mapping["marital_status"]),
                credit_history=row.get(model_cvs_mapping["credit_history"]),
                personal_risk_level=row.get(model_cvs_mapping["personal_risk_level"]),
                account_creation_date=datetime.strptime(row[model_cvs_mapping["account_creation_date"]], "%Y-%m-%d").date(),
                credit_score=float(row[model_cvs_mapping["credit_score"]]) if not pd.isna(row[model_cvs_mapping["credit_score"]]) else None,
                monthly_rent=float(row[model_cvs_mapping["monthly_rent"]]) if not pd.isna(row[model_cvs_mapping["monthly_rent"]]) else None,
                requested_loan_amount=float(row[model_cvs_mapping["requested_loan_amount"]]),
                region_id=region.id
            )

            db.add(borrower)

        db.commit()
        print("✅ Importation terminée.")
    except Exception as e:
        db.rollback()
        print("❌ Erreur :", e)
    finally:
        db.close()

if __name__ == "__main__":
    db_create()
    load_data(os.path.join(CURRENT_DIR, "data.csv"))

