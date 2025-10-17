from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from .database import Base


# ------------------------------------------------
# Define your model (ORM way)
# ------------------------------------------------
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text as sql_text
from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()
class Sahayak(Base):
    __tablename__ = "sahayak"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, index=True, nullable=False)
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
    password_hash = Column(String)
    is_approved = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
    updated_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP")
    is_active = Column(Boolean, default=False)