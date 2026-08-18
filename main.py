from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def home():
    return {"message": "IPO Tracker API is running!"}

@app.post("/check-allotment")
def check_allotment(data: dict):
    pan = data.get("pan")
    # Yahan aap apna scraping ya checking logic likhenge
    return {
        "pan": pan,
        "status": "Allotted",
        "shares": 150
    }

if __name__ == "__main__":
    uvicorn.run("main", host="0.0.0.0", port=8000)