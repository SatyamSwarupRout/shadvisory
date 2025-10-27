from pydantic import BaseModel
from typing import List, Optional


class SahayakBase(BaseModel):
    phone_number: str
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    aadhaar_number: Optional[str] = None
    village: Optional[str] = None
    block_name: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[int] = None
    gender_category: Optional[str] = None
    education_level: Optional[str] = None
    is_active: bool = True
    is_approved: bool = False

class SahayakCreate(BaseModel):
    phone_number: str
    
    
class SahayakUpdate(BaseModel):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    aadhaar_number: Optional[str] = None
    village: Optional[str] = None
    block_name: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[int] = None
    gender_category: Optional[str] = None
    education_level: Optional[str] = None
    is_active: Optional[bool] = None
    is_approved: Optional[bool] = None

#------------------------------------------------
# Farmer Classes
#------------------------------------------------
class FarmerBase(BaseModel):
    phone_number: str
    sahayak_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    aadhaar_number: Optional[str] = None
    village: Optional[str] = None
    block_name: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[int] = None
    gender_category: Optional[str] = None
    is_active: bool = True
    is_approved: bool = False


class FarmerCreate(BaseModel):
    phone_number: str
    sahayak_phone_number: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    aadhaar_number: Optional[str] = None
    village: Optional[str] = None
    block_name: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[int] = None
    gender_category: Optional[str] = None
    is_active: bool = True
    is_approved: bool = False

class FarmerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    aadhaar_number: Optional[str] = None
    village: Optional[str] = None
    block_name: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[int] = None
    gender_category: Optional[str] = None
    is_active: Optional[bool] = None
    is_approved: Optional[bool] = None
