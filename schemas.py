from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# =========================
# Authentication
# =========================

class UserRegister(BaseModel):
    name: str = Field(
        description="Full name of the user",
        examples=["Lavanya Reddy"]
    )
    email: EmailStr = Field(
        description="Valid email address",
        examples=["lavanya@gmail.com"]
    )
    password: str = Field(
        min_length=6,
        description="Password with minimum 6 characters",
        examples=["password123"]
    )
    role: str = Field(
        default="doctor",
        description="User role: admin or doctor",
        examples=["doctor"]
    )


class UserLogin(BaseModel):
    email: EmailStr = Field(
        description="Registered email address",
        examples=["lavanya@gmail.com"]
    )
    password: str = Field(
        description="User password",
        examples=["password123"]
    )


class Token(BaseModel):
    access_token: str = Field(
        description="JWT access token"
    )
    token_type: str = Field(
        description="Authentication token type",
        examples=["bearer"]
    )


# =========================
# Doctor
# =========================

class DoctorCreate(BaseModel):
    name: str = Field(
        description="Doctor's full name",
        examples=["Dr. Rathi"]
    )
    specialization: str = Field(
        description="Doctor's medical specialization",
        examples=["Cardiology"]
    )
    email: EmailStr = Field(
        description="Unique doctor email address",
        examples=["rathi@gmail.com"]
    )
    is_active: bool = Field(
        default=True,
        description="Whether the doctor is currently active",
        examples=[True]
    )


class DoctorUpdate(BaseModel):
    name: str = Field(
        description="Doctor's full name",
        examples=["Dr. Rathi"]
    )
    specialization: str = Field(
        description="Doctor's medical specialization",
        examples=["Cardiology"]
    )
    email: EmailStr = Field(
        description="Unique doctor email address",
        examples=["rathi@gmail.com"]
    )
    is_active: bool = Field(
        default=True,
        description="Whether the doctor is currently active",
        examples=[True]
    )


class DoctorPatch(BaseModel):
    name: Optional[str] = Field(
        default=None,
        description="Doctor's full name",
        examples=["Dr. Rathi"]
    )
    specialization: Optional[str] = Field(
        default=None,
        description="Doctor's medical specialization",
        examples=["Cardiology"]
    )
    email: Optional[EmailStr] = Field(
        default=None,
        description="Unique doctor email address",
        examples=["rathi@gmail.com"]
    )
    is_active: Optional[bool] = Field(
        default=None,
        description="Whether the doctor is currently active",
        examples=[True]
    )


class DoctorResponse(BaseModel):
    id: int
    name: str
    specialization: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


# =========================
# Patient
# =========================

class PatientCreate(BaseModel):
    name: str = Field(
        description="Patient's full name",
        examples=["Meena"]
    )
    age: int = Field(
        gt=0,
        description="Patient age must be greater than 0",
        examples=[25]
    )
    phone: str = Field(
        pattern=r"^\d{10}$",
        description="10-digit patient phone number",
        examples=["8688094563"]
    )
    doctor_id: Optional[int] = Field(
        default=None,
        description="ID of the doctor assigned to the patient",
        examples=[1]
    )


class PatientUpdate(BaseModel):
    name: str = Field(
        description="Patient's full name",
        examples=["Meena"]
    )
    age: int = Field(
        gt=0,
        description="Patient age must be greater than 0",
        examples=[25]
    )
    phone: str = Field(
        pattern=r"^\d{10}$",
        description="10-digit patient phone number",
        examples=["8688094563"]
    )
    doctor_id: Optional[int] = Field(
        default=None,
        description="ID of the doctor assigned to the patient",
        examples=[1]
    )


class PatientPatch(BaseModel):
    name: Optional[str] = Field(
        default=None,
        description="Patient's full name",
        examples=["Meena"]
    )
    age: Optional[int] = Field(
        default=None,
        gt=0,
        description="Patient age must be greater than 0",
        examples=[25]
    )
    phone: Optional[str] = Field(
        default=None,
        pattern=r"^\d{10}$",
        description="10-digit patient phone number",
        examples=["8688094563"]
    )
    doctor_id: Optional[int] = Field(
        default=None,
        description="ID of the doctor assigned to the patient",
        examples=[1]
    )


class PatientResponse(BaseModel):
    id: int
    name: str
    age: int
    phone: str
    doctor_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


# =========================
# Pagination
# =========================

class DoctorListResponse(BaseModel):
    total: int
    page: int
    limit: int
    data: list[DoctorResponse]


class PatientListResponse(BaseModel):
    total: int
    page: int
    limit: int
    data: list[PatientResponse]


# =========================
# Appointment Schemas
# =========================

AppointmentStatus = Literal[
    "scheduled",
    "completed",
    "cancelled"
]


class AppointmentCreate(BaseModel):
    doctor_id: int = Field(
        description="ID of the doctor",
        examples=[1]
    )
    patient_id: int = Field(
        description="ID of the patient",
        examples=[1]
    )
    appointment_date: datetime = Field(
        description="Appointment date and time",
        examples=["2026-10-01T10:00:00"]
    )
    status: AppointmentStatus = Field(
        default="scheduled",
        description="Appointment status",
        examples=["scheduled"]
    )


class AppointmentUpdate(BaseModel):
    doctor_id: int = Field(
        description="ID of the doctor",
        examples=[1]
    )
    patient_id: int = Field(
        description="ID of the patient",
        examples=[1]
    )
    appointment_date: datetime = Field(
        description="Appointment date and time",
        examples=["2026-10-01T10:00:00"]
    )
    status: AppointmentStatus = Field(
        description="Appointment status",
        examples=["completed"]
    )


class AppointmentPatch(BaseModel):
    doctor_id: Optional[int] = Field(
        default=None,
        description="ID of the doctor",
        examples=[1]
    )
    patient_id: Optional[int] = Field(
        default=None,
        description="ID of the patient",
        examples=[1]
    )
    appointment_date: Optional[datetime] = Field(
        default=None,
        description="Appointment date and time",
        examples=["2026-10-01T10:00:00"]
    )
    status: Optional[AppointmentStatus] = Field(
        default=None,
        description="Appointment status",
        examples=["scheduled"]
    )


class AppointmentResponse(BaseModel):
    id: int
    doctor_id: int
    patient_id: int
    appointment_date: datetime
    status: AppointmentStatus
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)