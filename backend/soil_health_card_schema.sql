
-- Table: Farmer
CREATE TABLE Farmer (
    farmer_id INTEGER  PRIMARY KEY,
    name TEXT NOT NULL,
    aadhaar_number TEXT,
    phone_number TEXT,
    address TEXT
);

-- Table: LandParcel
CREATE TABLE LandParcel (
    parcel_id INTEGER PRIMARY KEY,
    farmer_id INT REFERENCES Farmer(farmer_id),
    survey_number TEXT,
    area_hectares FLOAT,
    soil_type TEXT,
    irrigation_type TEXT,
    location_lat FLOAT,
    location_lon FLOAT
);

-- Table: SoilSample
CREATE TABLE SoilSample (
    sample_id INTEGER PRIMARY KEY,
    sample_official_id TEXT,
    parcel_id INT REFERENCES LandParcel(parcel_id),
    sample_date DATE,
    depth_cm INT
);

-- Table: SoilTestResult
CREATE TABLE SoilTestResult (
    result_id INTEGER PRIMARY KEY,
    -- sample_id INT REFERENCES SoilSample(sample_id),
    sample_date TEXT,
    area_acres FLOAT,
    irrigation_type TEXT,
    -- location_lon FLOAT,
    -- location_lat FLOAT,
    pH FLOAT,
    ec_ds_m FLOAT,
    organic_carbon_pct FLOAT,
    nitrogen_kg_ha FLOAT,
    phosphorus_kg_ha FLOAT,
    potassium_kg_ha FLOAT,
    sulfur_kg_ha FLOAT,
    zinc_ppm FLOAT,
    boron_ppm FLOAT,
    iron_ppm FLOAT,
    manganese_ppm FLOAT,
    copper_ppm FLOAT
    
);




-- Table: FertilizerRecommendation
CREATE TABLE FertilizerRecommendation (
    recommendation_id INTEGER PRIMARY KEY,
    result_id INT REFERENCES SoilTestResult(result_id),
    crop_type TEXT,
    urea_kg_ha FLOAT,
    dap_kg_ha FLOAT,
    mop_kg_ha FLOAT,
    gypsum_kg_ha FLOAT,
    compost_ton_ha FLOAT
);

-- Table: MicronutrientRecommendation
CREATE TABLE MicronutrientRecommendation (
    micro_id INTEGER PRIMARY KEY,
    recommendation_id INT REFERENCES FertilizerRecommendation(recommendation_id),
    zinc_sulfate_kg_ha FLOAT,
    borax_kg_ha FLOAT,
    ferrous_sulfate_kg_ha FLOAT
);

-- Table: Advisory
CREATE TABLE Advisory (
    advisory_id INTEGER PRIMARY KEY,
    recommendation_id INT REFERENCES FertilizerRecommendation(recommendation_id),
    advisory_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crop Specific requirements
CREATE TABLE CropRequirements (
  crop_name TEXT PRIMARY KEY,
  nitrogen_req FLOAT,
  phosphorus_req FLOAT,
  potassium_req FLOAT,
  sulfur_req FLOAT,
  zinc_req FLOAT,
  iron_req FLOAT,
  boron_req FLOAT,
  copper_req FLOAT
);

