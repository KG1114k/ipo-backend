from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Request body structure define karne ke liye
class AllotmentRequest(BaseModel):
    pan: str
    ipo_id: str

@app.get("/")
def home():
    return {"message": "IPO Tracker Backend is running successfully!"}

@app.post("/check-allotment")
def check_allotment(data: AllotmentRequest):
    pan = data.pan.upper()
    ipo_id = data.ipo_id

    if len(pan) != 10:
        raise HTTPException(status_code=400, detail="Invalid PAN number length")

    # TODO: Yahan aapko BSE ya Registrar (Link Intime/KFintech) ki site ka 
    # scraping ya API fetching logic likhna hoga.
    
    # Abhi ke liye testing ke taur par hum ek dummy logic de rahe hain:
    # (Aap yahan BeautifulSoup ya Selenium ka code add kar sakte hain)
    
    is_allotted = True if "A" in pan else False # Sample logic
    shares_count = 150 if is_allotted else 0

    return {
        "pan": pan,
        "ipo_id": ipo_id,
        "status": "Allotted" if is_allotted else "Not Allotted",
        "shares": shares_count
    }

if __name__ == "__main__":
    uvicorn.run("main", host="0.0.0.0", port=8000)