from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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

@app.post("/check-allotment")
async def check_allotment(data: AllotmentRequest):
    pan = data.pan.strip().upper()
    ipo_id = data.ipo_id

    if not pan or not ipo_id:
        raise HTTPException(status_code=400, detail="PAN and IPO ID are required")

    try:
        # NOTE: Registrars (KFintech, MUFG, Bigshare, BSE) ke paas direct public APIs nahi hoti, 
        # isliye production level par yahan scraping ya official endpoints integrate kiye jate hain.
        # Filhal testing aur smooth working ke liye hum logic-based simulation ya mock response de rahe hain:
        
        # Sample logic: Agar PAN ka length 10 hai toh status return karega
        if len(pan) == 10:
            # Aap yahan apna custom check ya database/registrar simulation laga sakte hain
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

@app.get("/")
def root():
    return {"message": "IPO Tracker Backend is running successfully!"}