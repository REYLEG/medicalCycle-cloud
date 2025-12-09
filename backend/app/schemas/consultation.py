"""Consultation schemas"""
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional
from enum import Enum


class ConsultationStatus(str, Enum):
    """Consultation status"""
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ConsultationBase(BaseModel):
    """Base consultation schema"""
    consultation_date: datetime
    status: ConsultationStatus = ConsultationStatus.SCHEDULED
    reason: Optional[str] = None
    chief_complaint: Optional[str] = None
    diagnosis: Optional[str] = None
    clinical_notes: Optional[str] = None
    vital_signs: Optional[str] = None
    physical_examination: Optional[str] = None
    treatment_plan: Optional[str] = None
    follow_up_date: Optional[datetime] = None


class ConsultationCreate(ConsultationBase):
    """Consultation creation schema"""
    patient_id: UUID
    doctor_id: UUID


class ConsultationUpdate(BaseModel):
    """Consultation update schema"""
    status: Optional[ConsultationStatus] = None
    chief_complaint: Optional[str] = None
    diagnosis: Optional[str] = None
    clinical_notes: Optional[str] = None
    vital_signs: Optional[str] = None
    physical_examination: Optional[str] = None
    treatment_plan: Optional[str] = None
    follow_up_date: Optional[datetime] = None


class ConsultationResponse(ConsultationBase):
    """Consultation response schema"""
    id: UUID
    patient_id: UUID
    doctor_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
