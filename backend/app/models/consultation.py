"""Consultation model"""
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from enum import Enum as PyEnum
from app.db.base import Base


class ConsultationStatus(str, PyEnum):
    """Consultation status"""
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Consultation(Base):
    """Consultation model"""
    __tablename__ = "consultations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    consultation_date = Column(DateTime, nullable=False)
    status = Column(Enum(ConsultationStatus), default=ConsultationStatus.SCHEDULED, nullable=False)
    reason = Column(String(500), nullable=True)
    chief_complaint = Column(Text, nullable=True)
    diagnosis = Column(Text, nullable=True)
    clinical_notes = Column(Text, nullable=True)
    vital_signs = Column(Text, nullable=True)  # JSON format
    physical_examination = Column(Text, nullable=True)
    treatment_plan = Column(Text, nullable=True)
    follow_up_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    patient = relationship("Patient", back_populates="consultations", foreign_keys=[patient_id])
    doctor = relationship("User", foreign_keys=[doctor_id])
    prescriptions = relationship("Prescription", back_populates="consultation", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Consultation {self.id}>"
