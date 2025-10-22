from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, database, pydantic_classes 
from sqlalchemy.ext.declarative import declarative_base
from typing import List



Base = declarative_base()
engine = database.engine

# ------------------------------------------------
# FastAPI application
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "🚀 FastAPI + PostgreSQL + SQLAlchemy + Alembic running in Docker!"}

@app.get("/sahayaks")
def get_sahayaks(db: Session = Depends(database.get_db)):
    try:
        sahayaks = db.query(models.Sahayak).all()
        return sahayaks
    except Exception as e:
        print("❌ Error occurred while fetching Sahayaks:", e)
        return {"error": "Failed to fetch Sahayaks"}

@app.get("/sahayak/{phone}")
def get_sahayak(phone: str, db: Session = Depends(database.get_db)):
    try:
        sahayak = db.query(models.Sahayak).filter(models.Sahayak.phone_number == phone).first()
        sahayak_base = pydantic_classes.SahayakBase(
            phone_number=sahayak.phone_number,
            email=sahayak.email,
            first_name=sahayak.first_name,
            last_name=sahayak.last_name,
            aadhaar_number=sahayak.aadhaar_number,
            village=sahayak.village,
            block_name=sahayak.block_name,
            district=sahayak.district,
            state=sahayak.state,
            gender_category=sahayak.gender_category,
            education_level=sahayak.education_level,
            is_active=sahayak.is_active,
            is_approved=sahayak.is_approved,
            pincode=sahayak.pincode
        )
        return sahayak_base
    except Exception as e:
        print("❌ Error occurred while fetching Sahayak:", e)
        return {"error": "Failed to fetch Sahayak"}


@app.post("/register_sahayak")
def add_sahayak(sahayak: pydantic_classes.SahayakBase, db: Session = Depends(database.get_db)):
    try:
        db_sahayak = models.Sahayak(**sahayak.model_dump())
        db.add(db_sahayak)
        db.commit()
        db.refresh(db_sahayak)
        return {"id": db_sahayak.id, **sahayak.model_dump()}
    except Exception as e:
        print("❌ Error occurred while adding Sahayak:", e)
        return {"error": "Failed to add Sahayak"}
    
@app.post("/update_sahayak")
def update_sahayak(sahayak: pydantic_classes.SahayakBase, db: Session = Depends(database.get_db)):
    try:
        db_sahayak = models.Sahayak(**sahayak.model_dump())
        db.merge(db_sahayak)
        db.commit()
        db.refresh(db_sahayak)
        return {"id": db_sahayak.id, **sahayak.model_dump()}
    except Exception as e:
        print("❌ Error occurred while updating Sahayak:", e)
        return {"error": "Failed to add Sahayak"}



    
