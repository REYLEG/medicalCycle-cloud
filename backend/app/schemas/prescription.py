"""Prescription schemas"""
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional
from enum import Enum


class PrescriptionStatus(str, Enum):
    """Prescription status"""
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class PrescriptionBase(BaseModel):
    """Base prescription schema"""
    medication_name: str = Field(..., min_length=1, max_length=255)
    dosage: str = Field(..., min_length=1, max_length=100)
    frequency: str = Field(..., min_length=1, max_length=100)
    duration: str = Field(..., min_length=1, max_length=100)
    route: str = Field(..., min_length=1, max_length=50)
    quantity: Optional[int] = None
    refills: int = 0
    status: PrescriptionStatus = PrescriptionStatus.ACTIVE
    notes: Optional[str] = None
    contraindications: Optional[str] = None
    side_effects: Optional[str] = None
    expiry_date: Optional[datetime] = None


class PrescriptionCreate(PrescriptionBase):
    """Prescription creation schema"""
    patient_id: UUID
    doctor_id: UUID
    consultation_id: Optional[UUID] = None


class PrescriptionUpdate(BaseModel):
    """Prescription update schema"""
    status: Optional[PrescriptionStatus] = None
    notes: Optional[str] = None
    refills: Optional[int] = None
    expiry_date: Optional[datetime] = None


class PrescriptionDispense(BaseModel):
    """Prescription dispense schema"""
    dispensed_by: UUID


class PrescriptionResponse(PrescriptionBase):
    """Prescription response schema"""
    id: UUID
    patient_id: UUID
    doctor_id: UUID
    consultation_id: Optional[UUID] = None
    prescribed_date: datetime
    dispensed_date: Optional[datetime] = None
    dispensed_by: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
