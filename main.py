from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json


app = FastAPI()

# Patient Model for validation
class Patient(BaseModel):

    id: Annotated[str, Field(..., description="ID of the patient", examples=['P001'])]
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


# Update Model
class PatientUpdate(BaseModel):

    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female', 'others']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]




def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data


def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)


@app.get("/")
def hello():
    return {"message": "Patient Management System API"}


@app.get("/about")
def about():
    return {"message": "A fully functional API to manage your patient records"}


# Get all the patients
@app.get("/view")
def view():
    data = load_data()
    return data


# Get the specific patient by ID
@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="ID of the patient in the DB", example="P001")):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")


# Get Patients by Sorting or Filtering
@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description="Sort on the basis of height, weight or bmi"), order: str = Query('asc', description="sort in asc or desc order")):
    
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')
    
    data = load_data()

    sort_order = True if order == 'desc' else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data


# Create a new patient
@app.post('/create')
def create_patient(patient: Patient):
    
    # load data
    data = load_data()

    # check if patient already exits
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exits")

    # add new patient
    data[patient.id] = patient.model_dump(exclude=['id'])

    # save into the json file
    save_data(data)

    return JSONResponse(status_code=201, content={"message":"Patient Created successfully"})




@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()
    pid = patient_id.strip() # Handle hidden spaces

    if pid not in data:
        raise HTTPException(status_code=404, detail=f'Patient {pid} not found')
    
    # 1. Get current data
    current_patient_dict = data[pid]
    
    # 2. Extract only the fields sent in the request
    update_dict = patient_update.model_dump(exclude_unset=True)

    # 3. Update dictionary
    current_patient_dict.update(update_dict)

    # 4. Re-validate and Save
    current_patient_dict['id'] = pid 
    try:
        # This Pydantic call should trigger your BMI logic if it's in the Patient model
        validated_patient = Patient(**current_patient_dict)
        
        # Store back to JSON dictionary (excluding 'id' key if that's your format)
        data[pid] = validated_patient.model_dump(exclude={'id'})
        save_data(data)
        
        # SUCCESS: Return 200, not 422!
        return {"message": "Patient updated successfully"}
        
    except Exception as e:
        # If Pydantic validation fails (e.g. height is 0), this triggers
        raise HTTPException(status_code=422, detail=f"Validation Error: {str(e)}")
    





@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')

    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={"message": "patient deleted"})    