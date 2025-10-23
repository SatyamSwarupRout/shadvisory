from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, status, HTTPException
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
def list_sahayaks(db: Session = Depends(database.get_db)):
    try:
        sahayaks = db.query(models.Sahayak).all()
        return sahayaks
    except Exception as e:
        print("❌ Error occurred while fetching Sahayaks:", e)
        return {"error": "Failed to fetch Sahayaks"}

@app.get("/sahayak/fetch/{phone}")
def get_sahayak(phone: str, db: Session = Depends(database.get_db)):
    try:
        db_sahayak = db.query(models.Sahayak).filter(models.Sahayak.phone_number == phone).first()
        if db_sahayak is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sahayak not found")
        
        sahayak = pydantic_classes.SahayakBase(**db_sahayak.__dict__)
        return sahayak
    except Exception as e:
        print("❌ Error occurred while fetching Sahayak:", e)
        return {"error": "Failed to fetch Sahayak"}


@app.post("/register_sahayak")
def add_sahayak(sahayak: pydantic_classes.SahayakCreate, db: Session = Depends(database.get_db)):
    try:
        db_sahayak = models.Sahayak(**sahayak.model_dump())
        db.add(db_sahayak)
        db.commit()
        db.refresh(db_sahayak)
        return {"id": db_sahayak.id, **sahayak.model_dump()}
    except Exception as e:
        print("❌ Error occurred while adding Sahayak:", e)
        return {"error": "Failed to add Sahayak"}

@app.put("/sahayak/update/{phone}")
def update_sahayak(phone: str, sahayak: pydantic_classes.SahayakUpdate, db: Session = Depends(database.get_db)):
    try:
        db_sahayak = db.query(models.Sahayak).filter(models.Sahayak.phone_number == phone).first()
        if db_sahayak is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sahayak not found")

        if (db_sahayak.is_active == False):
            return {"error": "Cannot update inactive Sahayak"}
        
        sahayak_data = sahayak.dict(exclude_unset=True) # Only update provided fields
        for key, value in sahayak_data.items():
            setattr(db_sahayak, key, value)

        db.merge(db_sahayak)
        db.commit()
        db.refresh(db_sahayak)
        return db_sahayak
    except Exception as e:
        print("❌ Error occurred while updating Sahayak:", e)
        return {"error": "Failed to update Sahayak"}


@app.put("/sahayak/delete/{phone}")
def delete_sahayak(phone: str, db: Session = Depends(database.get_db)):
    try:
        db_sahayak = db.query(models.Sahayak).filter(models.Sahayak.phone_number == phone).first()
        if db_sahayak is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sahayak not found")

        # setattr(db_sahayak, str(models.Sahayak.is_active), False)
        setattr(db_sahayak, "is_active", False)

        db.merge(db_sahayak)
        db.commit()
        db.refresh(db_sahayak)
        return db_sahayak
    except Exception as e:
        print("❌ Error occurred while deleting Sahayak:", e)
        return {"error": "Failed to delete Sahayak"}


