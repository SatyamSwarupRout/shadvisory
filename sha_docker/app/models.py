from sqlalchemy import Column, Integer, String, Float, Boolean, TIMESTAMP, ForeignKey, UniqueConstraint, text as sql_text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .database import Base


# ------------------------------------------------
# Define your model (ORM way)
# ------------------------------------------------
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text as sql_text
from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

#------------------------------------------------
# Farmer model
#------------------------------------------------
class Farmer(Base):
    __tablename__ = "farmer"

    farmer_id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, index=True, unique=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    aadhaar_number = Column(String)
    village = Column(String)
    block_name = Column(String)
    district = Column(String)
    pincode = Column(Integer)
    state = Column(String)
    gender_category = Column(String)
    is_approved = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=sql_text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=sql_text("CURRENT_TIMESTAMP"), onupdate=sql_text("CURRENT_TIMESTAMP"))
    is_active = Column(Boolean, default=True)

     # Foreign key reference
    sahayak_id = Column(Integer, ForeignKey("sahayak.sahayak_id"), nullable=False)

    # Relationship back to Sahayak ( one Farmer -> one Sahayak)
    sahayak = relationship("Sahayak", back_populates="farmers")

    # NEW relationships
    parcels = relationship("LandParcel", back_populates="farmer", cascade="all, delete-orphan")
    soil_samples = relationship("SoilSample", back_populates="farmer", cascade="all, delete-orphan")


#------------------------------------------------
# Sahayak Model
#------------------------------------------------
class Sahayak(Base):
    __tablename__ = "sahayak"

    sahayak_id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, index=True, unique=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    aadhaar_number = Column(String)
    email = Column(String)
    village = Column(String)
    block_name = Column(String)
    district = Column(String)
    pincode = Column(Integer)
    state = Column(String)
    gender_category = Column(String)
    education_level = Column(String)
    is_profile_completed = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=sql_text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=sql_text("CURRENT_TIMESTAMP"), onupdate=sql_text("CURRENT_TIMESTAMP"))
 
    # Relationship to Sahayak (one Sahayak → many Farmers)
    farmers = relationship("Farmer", back_populates="sahayak")
# ------------------------------------------------
# Land Parcel model
# ------------------------------------------------
class LandParcel(Base):
    __tablename__ = "land_parcel"

    parcel_id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("farmer.farmer_id"), nullable=False)

    # Address / location fields (defaults to farmer's values if not provided)
    state = Column(String)
    district = Column(String)
    tehsil = Column(String)
    ri_circle = Column(String)
    village = Column(String)

    # Identification fields
    survey_no = Column(String)   # SurveyNo / Khata no (you can optionally split)
    khata_no = Column(String)
    plot_no = Column(String)

    # Area
    area = Column(Float)         # store numeric area
    area_unit = Column(String, default = "acre")   # e.g. hectare / acre

    created_at = Column(TIMESTAMP, server_default=sql_text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=sql_text("CURRENT_TIMESTAMP"), onupdate=sql_text("CURRENT_TIMESTAMP"))
    is_active = Column(Boolean, default=True)

    __table_args__ = (
        UniqueConstraint('farmer_id', 'plot_no', name='uq_farmer_plot'),
    )

    # Relationships
    farmer = relationship("Farmer", back_populates="parcels")
    soil_samples = relationship("SoilSample", back_populates="parcel", cascade="all, delete-orphan")


# ------------------------------------------------
# Soil Sample & Test Result model
# ------------------------------------------------
class SoilSample(Base):
    __tablename__ = "soil_sample"

    sample_id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("farmer.farmer_id"), nullable=False)
    parcel_id = Column(Integer, ForeignKey("land_parcel.parcel_id"), nullable=True)  # optional if not associated

    sample_date = Column(TIMESTAMP, nullable=False)
    test_result_date = Column(TIMESTAMP, nullable=True)  # default to sample_date when inserting if not provided
    sample_depth_cm = Column(Integer)

    # Test result numeric fields (nullable)
    ph = Column(Float)
    ec = Column(Float)
    n = Column(Float)
    p = Column(Float)
    k = Column(Float)
    zinc = Column(Float)
    copper = Column(Float)
    boron = Column(Float)
    sulfur = Column(Float)
    iron = Column(Float)
    manganese = Column(Float)

    created_at = Column(TIMESTAMP, server_default=sql_text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=sql_text("CURRENT_TIMESTAMP"), onupdate=sql_text("CURRENT_TIMESTAMP"))
    is_active = Column(Boolean, default=True)

    # Relationships
    farmer = relationship("Farmer", back_populates="soil_samples")
    parcel = relationship("LandParcel", back_populates="soil_samples")