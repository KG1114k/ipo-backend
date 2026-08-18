from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# PAN check karne ke liye request model
class AllotmentRequest(BaseModel):
    pan: str
    ipo_id: str

@app.get("/")
def read_root():
    return {"message": "IPO Tracker Backend is running successfully!"}

# 1. IPO List ka Route
@app.get("/get-active-ipos")
def get_active_ipos():
    # Aap yahan scrapers ya database se list la sakte hain
    # Filhal testing ke liye ye list return karega
    return {
        "ipos": [
            "Bagmane Prime Office REIT", 
            "Bajaj Housing Finance", 
            "Hyundai Motor India", 
            "Ola Electric"
        ]
    }

# 2. PAN Check karne ka Route
@app.post("/check-allotment")
def check_allotment(request: AllotmentRequest):
    # Yahan asli logic aayega, abhi ke liye test response
    print(f"Checking PAN: {request.pan} for IPO: {request.ipo_id}")
    return {
        "status": "Not Allotted", # Ya "Allotted"
        "shares": 0
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)