"""Patient schemas"""
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional
from enum import Enum


class BloodType(str, Enum):
    """Blood types"""
    O_NEGATIVE = "O-"
    O_POSITIVE = "O+"
    A_NEGATIVE = "A-"
    A_POSITIVE = "A+"
    B_NEGATIVE = "B-"
    B_POSITIVE = "B+"
    AB_NEGATIVE = "AB-"
    AB_POSITIVE = "AB+"


class PatientBase(BaseModel):
    """Base patient schema"""
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None
    blood_type: Optional[BloodType] = None
    address: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    allergies: Optional[str] = None
    chronic_conditions: Optional[str] = None
    family_history: Optional[str] = None
    insurance_number: Optional[str] = None
    insurance_provider: Optional[str] = None


class PatientCreate(PatientBase):
    """Patient creation schema"""
    user_id: UUID


class PatientUpdate(BaseModel):
    """Patient update schema"""
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None
    blood_type: Optional[BloodType] = None
    address: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    allergies: Optional[str] = None
    chronic_conditions: Optional[str] = None
    family_history: Optional[str] = None
    insurance_number: Optional[str] = None
    insurance_provider: Optional[str] = None


class PatientResponse(PatientBase):
    """Patient response schema"""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
