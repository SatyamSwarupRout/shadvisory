from pydantic import BaseModel
from typing import List

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
    gender_category: str
    education_level: str
    is_active: bool
    is_approved: bool
    pincode: int
