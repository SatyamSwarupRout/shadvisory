from pydantic import BaseModel
from typing import List, Optional

class SahayakBase(BaseModel):
    phone_number: str
    email: str
    first_name: str
    last_name: str
    aadhaar_number: str
    village: str
    block_name: str
    district: str
    state: str
    pincode: int
    gender_category: str
    education_level: str
    is_active: bool
    is_approved: bool

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
