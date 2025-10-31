from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
from . import models, database, pydantic_classes 
from sqlalchemy.ext.declarative import declarative_base
from typing import List
from sqlalchemy.exc import IntegrityError


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
# --- LAND PARCEL ENDPOINTS ---

@app.get("/parcels")
def list_parcels(db: Session = Depends(database.get_db)):
    try:
        parcels = db.query(models.LandParcel).all()
        return parcels
    except Exception as e:
        print("❌ Error occurred while fetching Parcels:", e)
        return {"error": "Failed to fetch Parcels"}

@app.get("/parcel/fetch_by_parcel_id/{parcel_id}")
def get_parcel(parcel_id: int, db: Session = Depends(database.get_db)):
    try:
        db_parcel = db.query(models.LandParcel).filter(models.LandParcel.parcel_id == parcel_id).first()
        if db_parcel is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parcel not found")
        return db_parcel
    except Exception as e:
        print("❌ Error occurred while fetching Parcel:", e)
        return {"error": "Failed to fetch Parcel"}

@app.get("/parcels/fetch_by_farmer_phone/{phone}")
def get_parcels_by_farmer(phone: str, db: Session = Depends(database.get_db)):
    try:
        db_farmer = db.query(models.Farmer).filter(models.Farmer.phone_number == phone).first()
        if not db_farmer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Farmer not found")
        parcels = db.query(models.LandParcel).filter(models.LandParcel.farmer_id == db_farmer.farmer_id).all()
        return parcels
    except Exception as e:
        print("❌ Error occurred while fetching Parcels by farmer:", e)
        return {"error": "Failed to fetch Parcels"}
    
@app.get("/parcels/fetch_by_farmer_id/{farmer_id}")
def get_parcels_by_farmer_id(farmer_id: int, db: Session = Depends(database.get_db)):
    try:
        db_farmer = db.query(models.Farmer).filter(models.Farmer.farmer_id == farmer_id).first()
        if not db_farmer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Farmer not found")
        parcels = db.query(models.LandParcel).filter(models.LandParcel.farmer_id == farmer_id).all()
        return parcels
    except Exception as e:
        print("❌ Error occurred while fetching Parcels by farmer_id:", e)
        return {"error": "Failed to fetch Parcels"}

@app.get("/parcels/fetch_by_plot_no/{plot_no}")
def get_parcels_by_plot_no(plot_no: str, db: Session = Depends(database.get_db)):
    try:
        # This returns all parcels that have this plot_no (could belong to different farmers).
        parcels = db.query(models.LandParcel).filter(models.LandParcel.plot_no == plot_no).all()
        if not parcels:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parcel(s) with this plot_no not found")
        return parcels
    except Exception as e:
        print("❌ Error occurred while fetching Parcels by plot_no:", e)
        return {"error": "Failed to fetch Parcels"}


@app.post("/parcel/create")
def add_parcel(parcel: pydantic_classes.LandParcelCreate, db: Session = Depends(database.get_db)):
    try:
        db_farmer = db.query(models.Farmer).filter(models.Farmer.phone_number == parcel.farmer_phone).first()
        if db_farmer is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Farmer not found")

        # If plot_no is provided, ensure uniqueness for this farmer
        payload = parcel.model_dump()
        plot_no = payload.get("plot_no")
        if plot_no is not None:
            existing = db.query(models.LandParcel).filter(
                models.LandParcel.farmer_id == db_farmer.farmer_id,
                models.LandParcel.plot_no == plot_no
            ).first()
            if existing:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail=f"Parcel with plot_no '{plot_no}' already exists for this farmer (parcel_id={existing.parcel_id})")

        db_parcel = models.LandParcel()
        db_parcel.farmer_id = db_farmer.farmer_id

        # apply defaults from farmer if parcel's fields are None (state, district, tehsil, village)
        for key, value in payload.items():
            if key == "farmer_phone":
                continue
            if value is None:
                if key == "state" and getattr(db_farmer, "state", None):
                    setattr(db_parcel, "state", db_farmer.state)
                    continue
                if key == "district" and getattr(db_farmer, "district", None):
                    setattr(db_parcel, "district", db_farmer.district)
                    continue
                if key == "tehsil" and getattr(db_farmer, "block_name", None):
                    setattr(db_parcel, "tehsil", db_farmer.block_name)
                    continue
                if key == "village" and getattr(db_farmer, "village", None):
                    setattr(db_parcel, "village", db_farmer.village)
                    continue
                # leave other None fields as None
            else:
                setattr(db_parcel, key, value)

        db.add(db_parcel)
        try:
            db.commit()
        except IntegrityError as ie:
            db.rollback()
            # If a race condition lets two parallel requests through, DB unique constraint will protect us here
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Parcel with same plot_no already exists for this farmer.")
        db.refresh(db_parcel)
        return {"id": db_parcel.parcel_id, **parcel.model_dump()}
    except HTTPException:
        # re-raise HTTP errors as-is
        raise
    except Exception as e:
        print("❌ Error occurred while adding Parcel:", e)
        return {"error": "Failed to add Parcel"}


@app.put("/parcel/update/{parcel_id}")
def update_parcel(parcel_id: int, parcel: pydantic_classes.LandParcelUpdate, db: Session = Depends(database.get_db)):
    try:
        db_parcel = db.query(models.LandParcel).filter(models.LandParcel.parcel_id == parcel_id).first()
        if db_parcel is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parcel not found")

        if (db_parcel.is_active == False):
            return {"error": "Cannot update inactive Parcel"}

        parcel_data = parcel.dict(exclude_unset=True)
        for key, value in parcel_data.items():
            setattr(db_parcel, key, value)

        db.merge(db_parcel)
        db.commit()
        db.refresh(db_parcel)
        return db_parcel
    except Exception as e:
        print("❌ Error occurred while updating Parcel:", e)
        return {"error": "Failed to update Parcel"}

@app.put("/parcel/delete/{parcel_id}")
def delete_parcel(parcel_id: int, db: Session = Depends(database.get_db)):
    try:
        db_parcel = db.query(models.LandParcel).filter(models.LandParcel.parcel_id == parcel_id).first()
        if db_parcel is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parcel not found")

        setattr(db_parcel, "is_active", False)
        db.merge(db_parcel)
        db.commit()
        db.refresh(db_parcel)
        return db_parcel
    except Exception as e:
        print("❌ Error occurred while deleting Parcel:", e)
        return {"error": "Failed to delete Parcel"}

@app.put("/parcel/undelete/{parcel_id}")
def undelete_parcel(parcel_id: int, db: Session = Depends(database.get_db)):
    try:
        db_parcel = db.query(models.LandParcel).filter(models.LandParcel.parcel_id == parcel_id).first()
        if db_parcel is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parcel not found")

        setattr(db_parcel, "is_active", True)
        db.merge(db_parcel)
        db.commit()
        db.refresh(db_parcel)
        return db_parcel
    except Exception as e:
        print("❌ Error occurred while undeleting Parcel:", e)
        return {"error": "Failed to undelete Parcel"}


# --- SOIL SAMPLE ENDPOINTS ---

@app.get("/soil_samples")
def list_soil_samples(db: Session = Depends(database.get_db)):
    try:
        samples = db.query(models.SoilSample).all()
        return samples
    except Exception as e:
        print("❌ Error occurred while fetching Soil Samples:", e)
        return {"error": "Failed to fetch Soil Samples"}

@app.get("/soil_sample/fetch_by_sample_id/{sample_id}")
def get_soil_sample(sample_id: int, db: Session = Depends(database.get_db)):
    try:
        db_sample = db.query(models.SoilSample).filter(models.SoilSample.sample_id == sample_id).first()
        if db_sample is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Soil sample not found")
        return db_sample
    except Exception as e:
        print("❌ Error occurred while fetching Soil Sample:", e)
        return {"error": "Failed to fetch Soil Sample"}

@app.get("/soil_samples/fetch_by_farmer_phone/{phone}")
def get_soil_samples_by_farmer(phone: str, db: Session = Depends(database.get_db)):
    try:
        db_farmer = db.query(models.Farmer).filter(models.Farmer.phone_number == phone).first()
        if not db_farmer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Farmer not found")
        samples = db.query(models.SoilSample).filter(models.SoilSample.farmer_id == db_farmer.farmer_id).all()
        return samples
    except Exception as e:
        print("❌ Error occurred while fetching Soil Samples by farmer:", e)
        return {"error": "Failed to fetch Soil Samples"}

@app.get("/soil_samples/fetch_by_parcel_id/{parcel_id}")
def get_soil_samples_by_parcel(parcel_id: int, db: Session = Depends(database.get_db)):
    try:
        samples = db.query(models.SoilSample).filter(models.SoilSample.parcel_id == parcel_id).all()
        return samples
    except Exception as e:
        print("❌ Error occurred while fetching Soil Samples by parcel:", e)
        return {"error": "Failed to fetch Soil Samples"}

from datetime import datetime as _dt

@app.post("/soil_sample/create")
def add_soil_sample(sample: pydantic_classes.SoilSampleCreate, db: Session = Depends(database.get_db)):
    try:
        # Resolve farmer (if farmer_phone was provided)
        farmer_id = None
        if sample.farmer_phone:
            db_farmer = db.query(models.Farmer).filter(models.Farmer.phone_number == sample.farmer_phone).first()
            if db_farmer is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Farmer not found")
            farmer_id = db_farmer.farmer_id

        # If parcel_id provided, ensure it exists and belongs to farmer (if farmer_id known)
        if sample.parcel_id:
            db_parcel = db.query(models.LandParcel).filter(models.LandParcel.parcel_id == sample.parcel_id).first()
            if db_parcel is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parcel not found")
            if farmer_id and db_parcel.farmer_id != farmer_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Parcel does not belong to the given farmer")

        db_sample = models.SoilSample()
        if farmer_id:
            db_sample.farmer_id = farmer_id
        elif sample.parcel_id:
            # derive farmer from parcel
            db_parcel = db.query(models.LandParcel).filter(models.LandParcel.parcel_id == sample.parcel_id).first()
            db_sample.farmer_id = db_parcel.farmer_id
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Either farmer_phone or parcel_id must be provided")

        db_sample.parcel_id = sample.parcel_id

        payload = sample.model_dump()
        # default test_result_date to sample_date if not provided
        sample_date_val = payload.get("sample_date")
        if payload.get("test_result_date") is None:
            payload["test_result_date"] = sample_date_val

        for key, value in payload.items():
            if key in ("farmer_phone",):
                continue
            setattr(db_sample, key, value)

        db.add(db_sample)
        db.commit()
        db.refresh(db_sample)
        return {"id": db_sample.sample_id, **sample.model_dump()}
    except Exception as e:
        print("❌ Error occurred while adding Soil Sample:", e)
        return {"error": "Failed to add Soil Sample"}

@app.put("/soil_sample/update/{sample_id}")
def update_soil_sample(sample_id: int, sample: pydantic_classes.SoilSampleUpdate, db: Session = Depends(database.get_db)):
    try:
        db_sample = db.query(models.SoilSample).filter(models.SoilSample.sample_id == sample_id).first()
        if db_sample is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Soil sample not found")

        if (db_sample.is_active == False):
            return {"error": "Cannot update inactive Soil Sample"}

        sample_data = sample.dict(exclude_unset=True)
        # if parcel_id updated, ensure it belongs to the same farmer
        if "parcel_id" in sample_data and sample_data["parcel_id"] is not None:
            db_parcel = db.query(models.LandParcel).filter(models.LandParcel.parcel_id == sample_data["parcel_id"]).first()
            if db_parcel is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parcel not found")
            if db_parcel.farmer_id != db_sample.farmer_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New parcel does not belong to the same farmer")

        for key, value in sample_data.items():
            setattr(db_sample, key, value)

        db.merge(db_sample)
        db.commit()
        db.refresh(db_sample)
        return db_sample
    except Exception as e:
        print("❌ Error occurred while updating Soil Sample:", e)
        return {"error": "Failed to update Soil Sample"}

@app.put("/soil_sample/delete/{sample_id}")
def delete_soil_sample(sample_id: int, db: Session = Depends(database.get_db)):
    try:
        db_sample = db.query(models.SoilSample).filter(models.SoilSample.sample_id == sample_id).first()
        if db_sample is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Soil sample not found")

        setattr(db_sample, "is_active", False)
        db.merge(db_sample)
        db.commit()
        db.refresh(db_sample)
        return db_sample
    except Exception as e:
        print("❌ Error occurred while deleting Soil Sample:", e)
        return {"error": "Failed to delete Soil Sample"}

@app.put("/soil_sample/undelete/{sample_id}")
def undelete_soil_sample(sample_id: int, db: Session = Depends(database.get_db)):
    try:
        db_sample = db.query(models.SoilSample).filter(models.SoilSample.sample_id == sample_id).first()
        if db_sample is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Soil sample not found")

        setattr(db_sample, "is_active", True)
        db.merge(db_sample)
        db.commit()
        db.refresh(db_sample)
        return db_sample
    except Exception as e:
        print("❌ Error occurred while undeleting Soil Sample:", e)
        return {"error": "Failed to undelete Soil Sample"}