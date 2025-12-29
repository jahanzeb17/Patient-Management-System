from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class PatientBase(BaseModel):

    name: Annotated[str, Field(..., description='Name of the patient')]
    city: Annotated[str, Field(..., description="City where the patient is living")]
    age: Annotated[int, Field(..., gt=0, lt=100, description='Age of the patient')]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description="Gender of the patient")]  # Literal is used for Options
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in mtrs')]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the patient in kgs")]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2), 2)
        return bmi
    

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Normal"
        else:
            return "Obese"
        


class UpdatePatient(BaseModel):

    name: Optional[str] = None
    city: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[Literal['male', 'female', 'others']] = None
    height: Optional[float] = None
    weight: Optional[float] = None

        

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/view", status_code=status.HTTP_200_OK)
async def get_all_data(db: db_dependency):
    patients = db.query(models.Patient).all()
    return patients


@app.get("/view/{patient_id}", status_code=status.HTTP_200_OK)
async def get_single_patient(patient_id: int, db: db_dependency):
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient


@app.post("/create/", status_code=status.HTTP_201_CREATED)
async def create_patient(patient: PatientBase, db: db_dependency):
    db_patient = models.Patient(**patient.dict())
    db.add(db_patient)
    db.commit()


@app.put("/update/{patient_id}", status_code=status.HTTP_200_OK)
def update_patient(patient_id: int, patient_data: UpdatePatient, db: db_dependency):
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if patient_id is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    update_data = patient_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_patient, key, value)
    
    if "height" in update_data or "weight" in update_data:

        db_patient.bmi = db_patient.weight/(db_patient.height**2)

        if db_patient.bmi < 18.5: db_patient.verdict = "Underweight"
        elif db_patient.bmi < 25: db_patient.verdict = "Healthy"
        else: db_patient.verdict = "Overweight"

    
    db.commit()
    db.refresh(db_patient)

    return db_patient


@app.delete("/delete/{patient_id}", status_code=status.HTTP_200_OK)
def delete_patient(patient_id: int, db: db_dependency):
    patient_db = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if patient_db is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    db.delete(patient_db)
    db.commit()