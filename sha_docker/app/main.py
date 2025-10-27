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
#-------------------------------------------------
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "🚀 FastAPI + PostgreSQL + SQLAlchemy + Alembic running in Docker!"}

# ------------------------------------------------
# Sahayak Endpoints
#-------------------------------------------------


# ------------------------------------------------
# List all Sahayaks
#-------------------------------------------------
@app.get("/sahayaks")
def list_sahayaks(db: Session = Depends(database.get_db)):
    try:
        sahayaks = db.query(models.Sahayak).all()
        return sahayaks
    except Exception as e:
        print("❌ Error occurred while fetching Sahayaks:", e)
        return {"error": "Failed to fetch Sahayaks"}
    
# ------------------------------------------------
# Fetch a Sahayak by his phone number
#-------------------------------------------------
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

# ------------------------------------------------
# Register a Sahayak by his phone number
#-------------------------------------------------
@app.post("/register_sahayak")
def add_sahayak(sahayak: pydantic_classes.SahayakCreate, db: Session = Depends(database.get_db)):
    try:
        db_sahayak = models.Sahayak(**sahayak.model_dump())
        db.add(db_sahayak)
        db.commit()
        db.refresh(db_sahayak)
        return {"id": db_sahayak.sahayak_id, **sahayak.model_dump()}
    except Exception as e:
        print("❌ Error occurred while adding Sahayak:", e)
        return {"error": "Failed to add Sahayak"}
    
# ------------------------------------------------
# Update a Sahayak by his phone number
#-------------------------------------------------
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

# ------------------------------------------------
# Delete a Sahayak by his phone number
#-------------------------------------------------
@app.put("/sahayak/delete/{phone}")
def delete_sahayak(phone: str, db: Session = Depends(database.get_db)):
    # Deactivate the Sahayak, instead of deleting permanently
    # Set is_active to False
    #
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
# ------------------------------------------------
# Undelete a Sahayak by his phone number
#-------------------------------------------------
@app.put("/sahayak/undelete/{phone}")
def undelete_sahayak(phone: str, db: Session = Depends(database.get_db)):
    # Reactivate the Sahayak
    # Set is_active to True
    #   Only Admin can undelete/reactivate a Sahayak
    #
    try:
        db_sahayak = db.query(models.Sahayak).filter(models.Sahayak.phone_number == phone).first()
        if db_sahayak is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sahayak not found")

        setattr(db_sahayak, "is_active", True)

        db.merge(db_sahayak)
        db.commit()
        db.refresh(db_sahayak)
        return db_sahayak
    except Exception as e:
        print("❌ Error occurred while undeleting Sahayak:", e)
        return {"error": "Failed to undelete Sahayak"}
    
    
# ------------------------------------------------
# Farmer Endpoints
#-------------------------------------------------

# ------------------------------------------------
# List all Farmers
#-------------------------------------------------
@app.get("/farmers")
def list_farmers(db: Session = Depends(database.get_db)):
    try:
        farmers = db.query(models.Farmer).all()
        return farmers
    except Exception as e:
        print("❌ Error occurred while fetching Farmers:", e)
        return {"error": "Failed to fetch Farmers"}

# ------------------------------------------------
# Fetch a farmer by his phone number
#-------------------------------------------------
@app.get("/farmer/fetch/{phone}")
def get_farmer(phone: str, db: Session = Depends(database.get_db)):
    try:
        db_farmer = db.query(models.Farmer).filter(models.Farmer.phone_number == phone).first()
        if db_farmer is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Farmer not found")

        farmer = pydantic_classes.FarmerBase(**db_farmer.__dict__)
        return farmer
    except Exception as e:
        print("❌ Error occurred while fetching Farmer:", e)
        return {"error": "Failed to fetch Farmer"}

# ------------------------------------------------
# Register a Farmer by his phone number
#-------------------------------------------------
@app.post("/register_farmer")
def add_farmer(farmer: pydantic_classes.FarmerCreate, db: Session = Depends(database.get_db)):
    try:
        db_sahayak = db.query(models.Sahayak).filter(models.Sahayak.phone_number == farmer.sahayak_phone_number).first()
        if db_sahayak is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sahayak not found")
       
        db_farmer = models.Farmer()
        db_farmer.sahayak_id = db_sahayak.sahayak_id
        # Set other fields if provided
        for key, value in farmer.model_dump().items():
            if key != "sahayak_phone_number":
                setattr(db_farmer, key, value)  

        db.add(db_farmer)
        db.commit()
        db.refresh(db_farmer)
        return {"id": db_farmer.farmer_id, **farmer.model_dump()}
    except Exception as e:
        print("❌ Error occurred while adding Farmer:", e)
        return {"error": "Failed to add Farmer"}

# ------------------------------------------------
# Update a Farmer by his phone number
#-------------------------------------------------
@app.put("/farmer/update/{phone}")
def update_farmer(phone: str, farmer: pydantic_classes.FarmerUpdate, db: Session = Depends(database.get_db)):
    try:
        db_farmer = db.query(models.Farmer).filter(models.Farmer.phone_number == phone).first()
        if db_farmer is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Farmer not found")

        if (db_farmer.is_active == False):
            return {"error": "Cannot update inactive Farmer"}

        farmer_data = farmer.dict(exclude_unset=True) # Only update provided fields
        for key, value in farmer_data.items():
            setattr(db_farmer, key, value)

        db.merge(db_farmer)
        db.commit()
        db.refresh(db_farmer)
        return db_farmer
    except Exception as e:
        print("❌ Error occurred while updating Farmer:", e)
        return {"error": "Failed to update Farmer"}

# ------------------------------------------------
# Delete a Farmer by his phone number
#-------------------------------------------------
@app.put("/farmer/delete/{phone}")
def delete_farmer(phone: str, db: Session = Depends(database.get_db)):
    # Deactivate the Farmer, instead of deleting permanently
    # Set is_active to False
    #
    try:
        db_farmer = db.query(models.Farmer).filter(models.Farmer.phone_number == phone).first()
        if db_farmer is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Farmer not found")

        # setattr(db_farmer, str(models.Farmer.is_active), False)
        setattr(db_farmer, "is_active", False)

        db.merge(db_farmer)
        db.commit()
        db.refresh(db_farmer)
        return db_farmer
    except Exception as e:
        print("❌ Error occurred while deleting Farmer:", e)
        return {"error": "Failed to delete Farmer"}
# ------------------------------------------------
# Undelete a Farmer by his phone number
#-------------------------------------------------
@app.put("/farmer/undelete/{phone}")
def undelete_farmer(phone: str, db: Session = Depends(database.get_db)):
    # Reactivate the Farmer
    # Set is_active to True
    #   Only Admin can undelete/reactivate a Farmer
    #
    try:
        db_farmer = db.query(models.Farmer).filter(models.Farmer.phone_number == phone).first()
        if db_farmer is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Farmer not found")

        setattr(db_farmer, "is_active", True)

        db.merge(db_farmer)
        db.commit()
        db.refresh(db_farmer)
        return db_farmer
    except Exception as e:
        print("❌ Error occurred while undeleting Farmer:", e)
        return {"error": "Failed to undelete Farmer"}
