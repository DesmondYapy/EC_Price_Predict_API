curl -X 'POST' \
  'http://localhost:8000/predict' \
  -H 'Content-Type: application/json' \
  -d '{
    "project_name": "TURQUOISE",
    "area": 203.0,
    "floor_range": "01-05",
    "type_of_sale": 3,
    "district": 4,
    "street": "COVE DRIVE",
    "no_of_units": 1,
    "latitude": 1.278676,
    "longitude": 103.854735,
    "lease_year": "2007",
    "contract_date": "0715"
}'
