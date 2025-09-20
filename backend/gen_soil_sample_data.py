import random
from datetime import datetime, timedelta

def generate_soil_sample_inserts(n=100):
    start_date = datetime(2025, 6, 1)
    end_date = datetime(2025, 6, 30)
    delta_days = (end_date - start_date).days

    inserts = []
    for _ in range(n):
        parcel_id = random.randint(1, 300)
        sample_date = (start_date + timedelta(days=random.randint(0, delta_days))).strftime('%Y-%m-%d')
        depth_cm = round(random.uniform(1.0, 40.0), 2)
        sql = f"INSERT INTO SoilSample (rowid, parcel_id, sample_date, depth_cm) VALUES (NULL, {parcel_id}, '{sample_date}', {depth_cm});"
        inserts.append(sql)
    
    return inserts

# Example usage
if __name__ == "__main__":
    soil_sample_inserts = generate_soil_sample_inserts(100)
    for insert in soil_sample_inserts:
        print(insert)
