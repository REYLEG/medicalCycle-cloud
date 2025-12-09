"""Patient model"""
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from enum import Enum as PyEnum
from app.db.base import Base


class BloodType(str, PyEnum):
    """Blood types"""
    O_NEGATIVE = "O-"
    O_POSITIVE = "O+"
    A_NEGATIVE = "A-"
    A_POSITIVE = "A+"
    B_NEGATIVE = "B-"
    B_POSITIVE = "B+"
    AB_NEGATIVE = "AB-"
    AB_POSITIVE = "AB+"


class Patient(Base):
    """Patient model"""
    __tablename__ = "patients"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True)
    date_of_birth = Column(DateTime, nullable=True)
    gender = Column(String(20), nullable=True)
    blood_type = Column(Enum(BloodType), nullable=True)
    address = Column(String(500), nullable=True)
    city = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    country = Column(String(100), nullable=True)
    emergency_contact_name = Column(String(255), nullable=True)
    emergency_contact_phone = Column(String(20), nullable=True)
    allergies = Column(Text, nullable=True)  # JSON or comma-separated
    chronic_conditions = Column(Text, nullable=True)  # JSON or comma-separated
    family_history = Column(Text, nullable=True)
    insurance_number = Column(String(100), nullable=True)
    insurance_provider = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    consultations = relationship("Consultation", back_populates="patient", cascade="all, delete-orphan")
    prescriptions = relationship("Prescription", back_populates="patient", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Patient {self.id}>"
