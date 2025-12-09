"""Prescription model"""
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from enum import Enum as PyEnum
from app.db.base import Base


class PrescriptionStatus(str, PyEnum):
    """Prescription status"""
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class Prescription(Base):
    """Prescription model"""
    __tablename__ = "prescriptions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    consultation_id = Column(UUID(as_uuid=True), ForeignKey("consultations.id"), nullable=True)
    doctor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    medication_name = Column(String(255), nullable=False)
    dosage = Column(String(100), nullable=False)
    frequency = Column(String(100), nullable=False)  # e.g., "3 times daily"
    duration = Column(String(100), nullable=False)  # e.g., "7 days"
    route = Column(String(50), nullable=False)  # oral, injection, topical, etc.
    quantity = Column(Integer, nullable=True)
    refills = Column(Integer, default=0, nullable=False)
    status = Column(Enum(PrescriptionStatus), default=PrescriptionStatus.ACTIVE, nullable=False)
    notes = Column(Text, nullable=True)
    contraindications = Column(Text, nullable=True)
    side_effects = Column(Text, nullable=True)
    prescribed_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    expiry_date = Column(DateTime, nullable=True)
    dispensed_date = Column(DateTime, nullable=True)
    dispensed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    patient = relationship("Patient", back_populates="prescriptions", foreign_keys=[patient_id])
    consultation = relationship("Consultation", back_populates="prescriptions", foreign_keys=[consultation_id])
    doctor = relationship("User", foreign_keys=[doctor_id])
    pharmacist = relationship("User", foreign_keys=[dispensed_by])
    
    def __repr__(self):
        return f"<Prescription {self.id}>"
