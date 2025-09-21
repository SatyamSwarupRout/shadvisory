import os
import re 
from glob import iglob
import pandas as pd
import xml.etree.ElementTree as ET
import numpy as np
import sqlite3

DB_PATH = "soil_health_reco.db"

def df_2_sql_db(data_frame, table_name, replace_content=False):
    try:
        conn = sqlite3.connect(DB_PATH)
        if_exists_action = 'replace' if replace_content else 'append'
        data_frame.to_sql(table_name, conn, if_exists=if_exists_action, index=False)

        # 4. Close the database connection
        conn.close()
    except ValueError:
        # Code to execute if a ValueError occurs
        print("Error: Invalid input type.")
    except Exception as e:
        # A general except block to catch any other unhandled exceptions
        # The exception object can be accessed via 'e'
        print(f"An unexpected error occurred: {e}")
    else:
        # Code to execute if no exceptions are raised in the try block
        print("Operation successful!")
    finally:
        # Code to execute regardless of whether an exception occurred or not
        # This is often used for cleanup operations, like closing files
        print("Execution of try-except block complete.")

# ---------- Database Setup ----------
DB_PATH = "soil_health_reco.db"
DB_TABLE_NAME = 'SoilTestResult'
base_path = 'sha_data/*.xml'

global_soil_database_df = pd.DataFrame()
soil_data_labels = ['Sample_Collection_Date', 'Land_Area', 'Irrigation_Rainfed1', 'Latitude', 'Longitude',
                    'pH', 'EC', 'Organic_Carbon_OC', 'Available_Nitrogen_N', 
                    'Available_Phosphorus_P', 'Available_Potassium_K', 'Available_Sulphur_S',
                    'Available_Zinc_Zn', 'Available_Boron_B', 'Available_Iron_Fe', 
                    'Available_Manganese_Mn', 'Available_Copper_Cu']

soil_data_renamed_labels = [ 'sample_date', 'area_acres', 'irrigation_type', 'location_latitude', 'location_longitude',
                    'pH', 'ec_ds_m', 'organic_carbon_pct', 'nitrogen_kg_ha', 
                    'phosphorus_kg_ha', 'potassium_kg_ha', 'sulfur_kg_ha',
                    'zinc_ppm', 'boron_ppm', 'iron_ppm', 
                    'manganese_ppm', 'copper_ppm']

soil_database_df = pd.DataFrame(columns=soil_data_labels)

for file_path in iglob(base_path, recursive=True):
    #print(file_path)
    #print(file_path)
    tree = ET.parse(file_path)
    
    #Print all the children of root element
    root = tree.getroot()
    
    #Display whole XML
    #print(ET.tostring(root, encoding='utf8').decode('utf8'))
    display_iter = root.iter('{SoilHealthCard}Details1')
    
    shc_info = next(display_iter)
    #regex to extract Lat/Long from string
    GeoPosition = shc_info.get('Textbox6')
    #print(GeoPosition)
    pattern = '\d+\.\d+'
    location = re.findall(pattern, GeoPosition)
    #Sample Data
    sample_data = [ shc_info.get('Sample_Collection_Date'),
                    shc_info.get('Land_Area'),
                    shc_info.get('Irrigation_Rainfed1'),
                    location[0] if len(location) > 0 else None,
                    location[1] if len(location) > 1 else None]
    #DataLabels
    #if(action == 0):
    #Adding Data and Datalabels from Soil Test Report
    display_iter = display_iter.__iter__()
    for temp_test_data in display_iter:
        sample_data.append(temp_test_data.get("TestValue1"))

    #prepare dataframe for 1 soilHealthCard
    soil_database_df = pd.concat([soil_database_df, pd.DataFrame([sample_data], columns=soil_data_labels)],ignore_index=True)

    #TO-DO
    #convert test values to numeric and fill missing values with NaN


print(soil_database_df.size)
table_name = 'SoilTestResult'
replace_content = False
soil_database_df.columns = soil_data_renamed_labels
df_2_sql_db(soil_database_df, table_name, replace_content)

