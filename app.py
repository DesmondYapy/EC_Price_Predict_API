from fastapi import FastAPI
from pydantic import BaseModel
from tabulate import tabulate
import joblib
import pandas as pd

# Initialize FastAPI app
app = FastAPI()

# Load the trained model and encoders
model = joblib.load('EC_price_model.pkl')
label_encoder_project_name = joblib.load('label_encoder_project_name.pkl')
label_encoder_street = joblib.load('label_encoder_street.pkl')
label_encoder_floor_range = joblib.load('label_encoder_floor_range.pkl')
scaler = joblib.load('scaler.pkl')  # Ensure you save and load the scaler as well

# Define a request body
class PriceInput(BaseModel):
    project_name: str
    area: float
    floor_range: str
    type_of_sale: int
    district: int
    street: str
    latitude: float
    longitude: float
    no_of_units: int
    lease_year: str
    contract_date: str 

# Request response
class APIResponse(BaseModel):
    predicted_price: float 

@app.post("/predict")
async def predict_price(input_data: PriceInput) -> APIResponse:
    # Prepare the input for prediction
    data = pd.DataFrame([input_data.dict()])
    
    # Feature engineering for input data
    data['contract_year'] = data['contract_date'].apply(lambda x: int(x[:2]) + 2000 if int(x[:2]) < 50 else 1900 + int(x[:2]))
    data['contract_date'] = pd.to_datetime(data['contract_date'].apply(lambda x: x[:2] + '/' + x[2:]), format='%m/%y')
    
    # Encode categorical variables using the fitted label encoders
    try:
        data.loc[:, 'project_name'] = label_encoder_project_name.transform(data['project_name'])
    except ValueError:
        data['project_name'] = -1  # Default label for unseen values

    try:
        data[:,'street'] = label_encoder_street.transform(data['street'])
    except ValueError:
        data['street'] = -1

    try:
        data[:,'floor_range'] = label_encoder_floor_range.transform(data['floor_range'])
    except ValueError:
        data['floor_range'] = -1
    
    data.loc[:, 'contract_year'] = data['contract_date'].dt.year
    data.loc[:, 'contract_month'] = data['contract_date'].dt.month

    # Drop unnecessary columns
    data = data.drop(['contract_date'], axis=1)

    dtypes_dict = {"project_name": int, "street": int, "floor_range": int}
    data = data.astype(dtypes_dict)

    # Standardize
    data.loc[:,['area', 'latitude', 'longitude']] = scaler.transform(data[['area', 'latitude', 'longitude']])

    # Make a prediction
    print(tabulate(data, headers = 'keys', tablefmt = 'psql'))
    price = model.predict(data)
    
    return {"predicted_price": price}