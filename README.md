## EC Price Prediction API

This project is an API built using FastAPI to predict the resale prices of Executive Condominiums (EC) in Singapore. The API uses a trained Machine Learning model to provide predictions based on various property attributes such as the project name, area, floor range, type of sale, district, and more.

## Features

- **Price Prediction:** The API predicts EC resale prices at two specific points in time:
  - 5 years after the lease commencement (Minimum Occupancy Period, MOP).
  - 10 years after the lease commencement (Privatization period).
- **RESTful API:** Exposes the prediction model through an easily accessible RESTful API endpoint.
- **Containerized Application:** The entire application is containerized using Docker, making it easy to deploy and run on any environment.

## Requirements

- Docker (ensure Docker is installed and running on your machine)

## Getting Started

Follow these steps to run the EC Price Prediction API on your local machine:

### 1. Clone the Repository from GitHub

`git clone https://github.com/yourusername/ec-price-prediction-api.git`

`cd ec-price-prediction-ap `

### 2. Build the Docker Image and Run the Container

`docker build -t ec-price-api .`

`docker run -d -p 8000:8000 ec-price-api`

### 3. Test the API

`bash test.sh`

### Additional Information

API Exposes: `POST /predict`

```
{
    "project_name": "TURQUOISE",
    "area": 203,
    "floor_range": "01-05",
    "type_of_sale": 3,
    "district": 4,
    "street": "COVE DRIVE",
    "no_of_units": 1,
    "latitude": 24997.82171918,
    "longitude": 28392.53051557,
    "lease_year": "2007",
    "contract_date": "0715"
}
```
