# main.py
from fastapi import FastAPI, Path, HTTPException, Query, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Annotated, Literal
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import json
import os # Keep os for environment variable access

# --- Database Imports ---
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import UniqueConstraint, func

# --- FastAPI App Instance ---
app = FastAPI()

# --- Database Configuration ---
# DATABASE_URL is expected to be set as an environment variable in the Docker container
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # This check is still good practice in case the env var isn't set for some reason
    raise ValueError("DATABASE_URL environment variable not set. Please ensure it's configured in docker-compose.yml.")

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Database Model (SQLAlchemy) ---
class AppointmentDB(Base):
    __tablename__ = "appointments"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    appointment_time = Column(DateTime(timezone=True), unique=True, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), default=func.now())

    __table_args__ = (UniqueConstraint('appointment_time', name='_appointment_time_uc'),)

    def __repr__(self):
        return f"<Appointment(id='{self.id}', name='{self.name}', time='{self.appointment_time}', status='{self.status}')>"

# Create database tables
def create_db_tables():
    Base.metadata.create_all(bind=engine)

# Dependency to get a DB session
def get_db():
    db = Session()
    try:
        yield db
    finally:

        db.close()

# --- Pydantic Model (for request/response validation) ---
class Appoint(BaseModel):
    id: Annotated[str, Field(..., description='Id of the patient', example='1')]
    name: Annotated[str, Field(..., description='Name of the patient')]
    email: Annotated[str, Field(..., description='Email of the patient', example='jane@example.com')]
    appointment_time: Annotated[datetime, Field(..., description='Appointment time of the patient', unique=True, example='2025-07-16T10:00:00Z')]
    status: Annotated[Literal['approved', 'rejected', 'pending'], Field('pending', description='Status of the appointment', example='pending')]

    class Config:
        json_schema_extra = {
            "example": {
                "id": "1",
                "name": "John Doe",
                "email": "john.doe@example.com",
                "appointment_time": "2025-07-22T10:00:00Z",
                "status": "pending"
            }
        }

# --- Startup Event Handler ---
@app.on_event("startup")
async def startup_event():
    create_db_tables()
    print("Database tables created/checked.")

# --- API Endpoints ---

@app.get("/view")
def view(db: Annotated[Session, Depends(get_db)]):
    appointments = db.query(AppointmentDB).all()
    return appointments

@app.get('/detail/{id}')
def view_appointment(db: Annotated[Session, Depends(get_db)], id: str = Path(..., description='Id of the Appointment ', examples='1'),
                    ):
    appointment = db.query(AppointmentDB).filter(AppointmentDB.id == id).first()
    if appointment:
        return appointment
    raise HTTPException(status_code=404, detail='No appointment found with this id')

@app.post("/create")
def create_appointment(new_appoint: Appoint, db: Annotated[Session,Depends(get_db)]):
    # CHECK IF APPOINTMENT ID ALREADY EXISTS
    existing_by_id = db.query(AppointmentDB).filter(AppointmentDB.id == new_appoint.id).first()
    if existing_by_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Appointment with ID {new_appoint.id} already exists')

   
   
    # Get current time in UTC and adjust to IST for business logic
    current_utc_time = datetime.now(timezone.utc)
    ist_offset = timedelta(hours=5, minutes=30)
    current_ist_time = current_utc_time + ist_offset

    today_ist_date = current_ist_time.date()

    appointment_dt_ist = new_appoint.appointment_time
    appointment_date = appointment_dt_ist.date()

    latest_allowed_date = today_ist_date + timedelta(days=2)

    new_appointment_time_utc = new_appoint.appointment_time
     # CHECK IF APPOINTMENT TIME ALREADY EXISTS
    existing_by_time = db.query(AppointmentDB).filter(AppointmentDB.appointment_time == new_appointment_time_utc).first()
    if existing_by_time:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Appointment time already exists')

    # Validate appointment date is today or within the next 2 days
    if not (today_ist_date <= appointment_date <= latest_allowed_date):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Appointment must be for today or within the next 2 days only (inclusive of today).")
    # Validate appointment time is on the hour and within business hours
    if not (9 <= appointment_dt_ist.hour < 19 and appointment_dt_ist.minute == 0):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Appointment time must be between 9:00 AM and 7:00 PM with 0 minutes (on the hour).")

    db_appointment = AppointmentDB(
        id=new_appoint.id,
        name=new_appoint.name,
        email=new_appoint.email,
        appointment_time=new_appointment_time_utc,
        status=new_appoint.status,
        created_at=current_ist_time
    )

    try:
        db.add(db_appointment)
        db.commit()
        db.refresh(db_appointment)
        return JSONResponse(status_code=status.HTTP_200_OK, content={'message': 'Appointment created successfully', 'appointment_id': db_appointment.id})
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {e}")


@app.put('/accept/{id}')
def accept_appointment(db: Annotated[Session, Depends(get_db)], id: str = Path(..., description='Id of the Appointment to accept', examples='1'),
                       ):
    appointment = db.query(AppointmentDB).filter(AppointmentDB.id == id).first()
    if appointment:
        appointment.status = 'approved'
        try:
            db.commit()
            db.refresh(appointment)
            return JSONResponse(status_code=status.HTTP_200_OK, content={'message': 'Appointment accepted successfully', 'appointment_id': appointment.id})
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {e}")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No appointment found with this id')

@app.put('/reject/{id}')
def reject_appointment(db: Annotated[Session, Depends(get_db)], id: str = Path(..., description='Id of the Appointment to reject', examples='1')):
    appointment = db.query(AppointmentDB).filter(AppointmentDB.id == id).first()
    if appointment:
        appointment.status = 'rejected'
        try:
            db.commit()
            db.refresh(appointment)
            return JSONResponse(status_code=status.HTTP_200_OK, content={'message': 'Appointment rejected successfully', 'appointment_id': appointment.id})
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {e}")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No appointment found with this id')

@app.get('/pending')
def get_pending_appointments(db: Annotated[Session, Depends(get_db)]):
    pending_appointments = db.query(AppointmentDB).filter(AppointmentDB.status == 'pending').all()
    return pending_appointments

@app.get('/approved')
def get_approved_appointments(db: Annotated[Session, Depends(get_db)]):
    approved_appointments = db.query(AppointmentDB).filter(AppointmentDB.status == 'approved').all()
    return approved_appointments

@app.get('/rejected')
def get_rejected_appointments(db: Annotated[Session, Depends(get_db)]):
    rejected_appointments = db.query(AppointmentDB).filter(AppointmentDB.status == 'rejected').all()
    return rejected_appointments
