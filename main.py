# app/main.py

from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
# from source.attorneys import Attorneys
from source.professionals import Attorneys, get_db
from starlette.middleware.cors import CORSMiddleware
from datetime import datetime

router = APIRouter()

# Initialize FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "sqlite:///D://Database backups//Trademark Websites//law_firms_data.db"


# Instantiate the DatabaseManager class with the SQLite database URL
# db_manager = Attorneys(DATABASE_URL)


@app.get("/get_companies/")
async def get_companies(db: Session = Depends(get_db)):
    professionals = Attorneys(db)
    companies = professionals.get_companies()
    companies = [company[0] for company in companies]
    designations = professionals.get_designations()
    designations = [designation[0] for designation in designations]
    services = professionals.get_services()
    services = [service[0] for service in services]
    return {"companies": companies, "designations": designations, "services": services}


@app.get("/get_designations/")
async def get_companies(db: Session = Depends(get_db)):
    professionals = Attorneys(db)
    companies = professionals.get_designations()
    companies = [company[0] for company in companies]
    return {"companies": companies, "total": len(companies)}


# API route to get all users
@app.get("/attorneys/")
def read_attorneys(db: Session = Depends(get_db)):
    professionals = Attorneys(db)
    attorneys = professionals.get_attorneys(limit=20)
    return [dict(zip(attorney._fields, attorney)) for attorney in attorneys]
#
#
# # API route to get a specific user by ID
# @app.get("/attorneys/{attorney_id}", response_model=Professionals)
# def read_user(attorney_id: int, db: Session = Depends(db_manager.get_db)):
#     attorney = db_manager.get_attorney_by_id(db, user_id=attorney_id)
#     if attorney is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return dict(zip(attorney.keys(), attorney))
