curl -X POST "http://localhost:8000/register_sahayak" \
     -H "Content-Type: application/json" \
     -d '{
     "phone_number": "55555555555",
     "email": "",
     "first_name": "",
     "last_name": "",
     "aadhaar_number": "",
     "village": "",
     "block_name": "",
     "district": "",
     "state": "",
     "gender_category": "",
     "education_level": "",
     "is_active": true,
     "is_approved": false,
     "pincode": 123456
}'

