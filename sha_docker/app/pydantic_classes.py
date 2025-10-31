from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

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

# ----------------------
# Land Parcel DTOs
# ----------------------
class LandParcelBase(BaseModel):
    farmer_id: Optional[int] = None
    state: Optional[str] = None
    district: Optional[str] = None
    tehsil: Optional[str] = None
    ri_circle: Optional[str] = None
    village: Optional[str] = None
    survey_no: Optional[str] = None
    khata_no: Optional[str] = None
    plot_no: Optional[str] = None
    area: Optional[float] = None
    area_unit: Optional[str] = None
    is_active: bool = True

class LandParcelCreate(BaseModel):
    farmer_phone: str                        # required to link -> resolved server-side
    state: Optional[str] = None
    district: Optional[str] = None
    tehsil: Optional[str] = None
    ri_circle: Optional[str] = None
    village: Optional[str] = None
    survey_no: Optional[str] = None
    khata_no: Optional[str] = None
    plot_no: str
    area: Optional[float] = None
    area_unit: Optional[str] = None
    is_active: bool = True

class LandParcelUpdate(BaseModel):
    state: Optional[str] = None
    district: Optional[str] = None
    tehsil: Optional[str] = None
    ri_circle: Optional[str] = None
    village: Optional[str] = None
    survey_no: Optional[str] = None
    khata_no: Optional[str] = None
    area: Optional[float] = None
    area_unit: Optional[str] = None
    is_active: Optional[bool] = None


# ----------------------
# Soil Sample DTOs
# ----------------------
class SoilSampleBase(BaseModel):
    farmer_id: Optional[int] = None
    parcel_id: Optional[int] = None
    sample_date: datetime
    test_result_date: Optional[datetime] = None
    sample_depth_cm: Optional[int] = None
    ph: Optional[float] = None
    ec: Optional[float] = None
    n: Optional[float] = None
    p: Optional[float] = None
    k: Optional[float] = None
    zinc: Optional[float] = None
    copper: Optional[float] = None
    boron: Optional[float] = None
    sulfur: Optional[float] = None
    iron: Optional[float] = None
    manganese: Optional[float] = None
    is_active: bool = True

class SoilSampleCreate(BaseModel):
    farmer_phone: Optional[str] = None   # server will resolve to farmer_id if provided
    parcel_id: Optional[int] = None
    sample_date: datetime
    test_result_date: Optional[datetime] = None
    sample_depth_cm: Optional[int] = None
    ph: Optional[float] = None
    ec: Optional[float] = None
    n: Optional[float] = None
    p: Optional[float] = None
    k: Optional[float] = None
    zinc: Optional[float] = None
    copper: Optional[float] = None
    boron: Optional[float] = None
    sulfur: Optional[float] = None
    iron: Optional[float] = None
    manganese: Optional[float] = None
    is_active: bool = True

class SoilSampleUpdate(BaseModel):
    #parcel_id: Optional[int] = None
    sample_date: Optional[datetime] = None
    test_result_date: Optional[datetime] = None
    sample_depth_cm: Optional[int] = None
    ph: Optional[float] = None
    ec: Optional[float] = None
    n: Optional[float] = None
    p: Optional[float] = None
    k: Optional[float] = None
    zinc: Optional[float] = None
    copper: Optional[float] = None
    boron: Optional[float] = None
    sulfur: Optional[float] = None
    iron: Optional[float] = None
    manganese: Optional[float] = None
    is_active: Optional[bool] = None