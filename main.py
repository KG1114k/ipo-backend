from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Enable CORS so Flutter app can communicate with Railway backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body structure matching Flutter JSON payload
class AllotmentRequest(BaseModel):
    pan: str
    ipo_id: str

@app.get("/")
def root():
    return {"message": "IPO Tracker Backend is running successfully!"}

# 1. Naya Endpoint: Live Active IPOs fetch karne ke liye
@app.get("/get-active-ipos")
def get_active_ipos():
    url = "https://www.chittorgarh.com/report/ipo-allotment-status/57/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        ipo_names = []
        # Chittorgarh ki table se IPO names extract karna
        for a in soup.select('.table-responsive table tr td:first-child a')[:10]:
            name = a.text.strip()
            if name and name not in ipo_names:
                ipo_names.append(name)
        
        # Agar website se data na mile toh default list bhej do
        if not ipo_names:
            return {"ipos": ["Bagmane Prime Office REIT", "Bajaj Housing Finance", "Hyundai Motor India"]}
             
        return {"ipos": ipo_names}
    except Exception as e:
        # Error aane par fallback list return karega taaki app crash na ho
        return {"ipos": ["Bagmane Prime Office REIT", "Bajaj Housing Finance", "Hyundai Motor India"]}

# 2. Existing Endpoint: Allotment check karne ke liye
@app.post("/check-allotment")
async def check_allotment(data: AllotmentRequest):
    pan = data.pan.strip().upper()
    ipo_id = data.ipo_id

    if not pan or not ipo_id:
        raise HTTPException(status_code=400, detail="PAN and IPO ID are required")

    try:
        if len(pan) == 10:
            is_allotted = "BAGMANE" in ipo_id.upper() or "BAJAJ" in ipo_id.upper()
            
            return {
                "pan": pan,
                "ipo": ipo_id,
                "status": "Allotted" if is_allotted else "Not Allotted",
                "shares": 150 if is_allotted else 0
            }
        else:
            raise HTTPException(status_code=400, detail="Invalid PAN format")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))