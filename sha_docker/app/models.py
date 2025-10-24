from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, text as sql_text
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
    is_approved = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=sql_text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=sql_text("CURRENT_TIMESTAMP"), onupdate=sql_text("CURRENT_TIMESTAMP"))
 
    # Relationship to Sahayak (one Sahayak → many Farmers)
    farmers = relationship("Farmer", back_populates="sahayak")