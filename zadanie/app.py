from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from models import Tire
from database import Base, engine, SessionLocal
import json

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Tire Control System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Tire Control System API"}

@app.get("/tires")
def get_tires():
    db = SessionLocal()
    tires = db.query(Tire).all()
    db.close()
    return tires

@app.post("/tires")
def add_tire(brand: str, diameter: float, pressure: float, status: str):
    db = SessionLocal()
    tire = Tire(brand=brand, diameter=diameter, pressure=pressure, status=status)
    db.add(tire)
    db.commit()
    db.refresh(tire)
    db.close()
    return tire

@app.delete("/tires/{tire_id}")
def delete_tire(tire_id: int):
    db = SessionLocal()
    tire = db.query(Tire).filter(Tire.id == tire_id).first()
    if not tire:
        db.close()
        raise HTTPException(status_code=404, detail="Tire not found")
    db.delete(tire)
    db.commit()
    db.close()
    return {"message": "Tire deleted"}

@app.post("/tires/upload_json")
async def upload_json(file: UploadFile = File(...)):
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Only JSON files are supported")

    contents = await file.read()
    try:
        data = json.loads(contents)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    if not isinstance(data, list):
        raise HTTPException(status_code=400, detail="JSON must be a list")

    db = SessionLocal()
    added = 0
    for item in data:
        try:
            tire = Tire(
                brand=item["brand"],
                diameter=float(item["diameter"]),
                pressure=float(item["pressure"]),
                status=item["status"]
            )
            db.add(tire)
            added += 1
        except:
            continue
    db.commit()
    db.close()
    return {"added": added}
