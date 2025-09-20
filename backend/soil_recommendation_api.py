# soil_recommendation_api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3
import pandas as pd

from constants import FERTILIZER

app = FastAPI(title="Soil Health Card Fertilizer Recommendation API")

# ---------- Database Setup ----------
DB_PATH = "soil_health_reco.db"

def get_crop_requirements():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM CropRequirements", conn)
    conn.close()
    return {
        row["crop_name"]: row for _, row in df.iterrows()
    }

def get_soil_test_result(result_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        query = f'SELECT * FROM SoilTestResult WHERE result_id="{result_id}"'
        df = pd.read_sql_query(query, conn)
        df_filled = df.fillna(0).replace('--', 0)
        conn.close()

        return df_filled
    
    except Exception as e:
        # A general except block to catch any other unhandled exceptions
        # The exception object can be accessed via 'e'
        print(f"An unexpected error occurred: {e}")


# ---------- Data Models ----------
class SoilTestResult(BaseModel):
    nitrogen_kg_ha: float
    phosphorus_kg_ha: float
    potassium_kg_ha: float
    sulfur_kg_ha: float
    zinc_ppm: float
    iron_ppm: float
    copper_ppm: float
    manganese_ppm: float
    boron_ppm: float

class RecommendationResponse(BaseModel):
    crop_name: str
    urea_kg_ha: float
    dap_kg_ha: float
    mop_kg_ha: float
    gypsum_kg_ha: float
    zinc_sulfate_kg_ha: float
    borax_kg_ha: float
    ferrous_sulfate_kg_ha: float

# ---------- Recommendation Logic ----------
def calculate_recommendation(soil: SoilTestResult, crop_row) -> RecommendationResponse:
    def max0(x): return max(float(x), 0.0)

    N_def = max0(crop_row["nitrogen_req"] - soil.nitrogen_kg_ha)
    P_def = max0(crop_row["phosphorus_req"] - soil.phosphorus_kg_ha)
    K_def = max0(crop_row["potassium_req"] - soil.potassium_kg_ha)

    urea_kg = round(N_def * FERTILIZER["N_IN_UREA"], 2)
    dap_kg = round(P_def * FERTILIZER["P_IN_DAP"], 2)
    mop_kg = round(K_def * FERTILIZER["K_IN_MOP"], 2)

    gypsum_kg = round(max0(crop_row["sulfur_req"] - soil.sulfur_kg_ha) * FERTILIZER["S_IN_GYPSUM"], 2)
    zinc_sulfate = round(max0(crop_row["zinc_req"] - soil.zinc_ppm) * FERTILIZER["Zn_IN_ZINC_SULFATE"], 2)
    borax = round(max0(crop_row["boron_req"] - soil.boron_ppm) * FERTILIZER["B_IN_BORAX"], 2)
    ferrous_sulfate = round(max0(crop_row["iron_req"] - soil.iron_ppm) * FERTILIZER["FE_IN_FERROUS_SULPHATE"], 2)

    return RecommendationResponse(
        crop_name=crop_row["crop_name"],
        urea_kg_ha=urea_kg,
        dap_kg_ha=dap_kg,
        mop_kg_ha=mop_kg,
        gypsum_kg_ha=gypsum_kg,
        zinc_sulfate_kg_ha=zinc_sulfate,
        borax_kg_ha=borax,
        ferrous_sulfate_kg_ha=ferrous_sulfate
    )

# ---------- API Routes ----------
@app.get("/recommend/{sample_id}", response_model=RecommendationResponse)
def recommend(sample_id):
    crop_name ='wheat'
    soil = get_soil_test_result(sample_id)
    crops = get_crop_requirements()
    if crop_name not in crops:
        raise HTTPException(status_code=404, detail=f"Crop '{crop_name}' not found in database")
    crop_row = crops[crop_name]
    return calculate_recommendation(soil, crop_row)

@app.get("/crops", response_model=List[str])
def list_crops():
    return list(get_crop_requirements().keys())
