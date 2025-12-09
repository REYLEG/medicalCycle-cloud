"""Prescription management routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from app.db.session import get_db
from app.models.user import User
from app.models.prescription import Prescription
from app.models.patient import Patient
from app.schemas.prescription import PrescriptionCreate, PrescriptionUpdate, PrescriptionDispense, PrescriptionResponse
from app.api.deps import get_current_user, get_current_doctor, get_current_pharmacist
from app.core.audit import log_audit
from app.models.audit_log import AuditAction

router = APIRouter(prefix="/prescriptions", tags=["prescriptions"])


@router.post("/", response_model=PrescriptionResponse, status_code=status.HTTP_201_CREATED)
def create_prescription(
    prescription_data: PrescriptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_doctor)
):
    """Create a new prescription (doctors only)"""
    # Verify patient exists
    patient = db.query(Patient).filter(Patient.id == prescription_data.patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    # Verify doctor exists
    doctor = db.query(User).filter(User.id == prescription_data.doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )
    
    prescription = Prescription(**prescription_data.dict())
    db.add(prescription)
    db.commit()
    db.refresh(prescription)
    
    log_audit(
        db=db,
        user_id=current_user.id,
        action=AuditAction.CREATE,
        resource_type="prescription",
        resource_id=prescription.id,
        description=f"Created prescription for patient: {patient.id}, medication: {prescription.medication_name}"
    )
    
    return prescription


@router.get("/", response_model=list[PrescriptionResponse])
def list_prescriptions(
    patient_id: UUID = None,
    status_filter: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List prescriptions with optional filters"""
    query = db.query(Prescription)
    
    if patient_id:
        query = query.filter(Prescription.patient_id == patient_id)
    
    if status_filter:
        query = query.filter(Prescription.status == status_filter)
    
    prescriptions = query.offset(skip).limit(limit).all()
    
    log_audit(
        db=db,
        user_id=current_user.id,
        action=AuditAction.READ,
        resource_type="prescription",
        description=f"Listed {len(prescriptions)} prescriptions"
    )
    
    return prescriptions


@router.get("/{prescription_id}", response_model=PrescriptionResponse)
def get_prescription(
    prescription_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get prescription by ID"""
    prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
    
    if not prescription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prescription not found"
        )
    
    # Verify access permissions
    patient = prescription.patient
    if (current_user.id != patient.user_id and 
        current_user.id != prescription.doctor_id and 
        current_user.role.value not in ["pharmacist", "admin"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this prescription"
        )
    
    log_audit(
        db=db,
        user_id=current_user.id,
        action=AuditAction.READ,
        resource_type="prescription",
        resource_id=prescription_id,
        description=f"Viewed prescription: {prescription_id}"
    )
    
    return prescription


@router.put("/{prescription_id}", response_model=PrescriptionResponse)
def update_prescription(
    prescription_id: UUID,
    prescription_data: PrescriptionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_doctor)
):
    """Update prescription (doctors only)"""
    prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
    
    if not prescription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prescription not found"
        )
    
    # Only the doctor who created it or admin can update
    if current_user.id != prescription.doctor_id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this prescription"
        )
    
    update_data = prescription_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(prescription, field, value)
    
    db.add(prescription)
    db.commit()
    db.refresh(prescription)
    
    log_audit(
        db=db,
        user_id=current_user.id,
        action=AuditAction.UPDATE,
        resource_type="prescription",
        resource_id=prescription_id,
        description=f"Updated prescription: {prescription_id}"
    )
    
    return prescription


@router.post("/{prescription_id}/dispense", response_model=PrescriptionResponse)
def dispense_prescription(
    prescription_id: UUID,
    dispense_data: PrescriptionDispense,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_pharmacist)
):
    """Dispense prescription (pharmacists only)"""
    prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
    
    if not prescription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prescription not found"
        )
    
    # Verify pharmacist exists
    pharmacist = db.query(User).filter(User.id == dispense_data.dispensed_by).first()
    if not pharmacist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pharmacist not found"
        )
    
    prescription.dispensed_date = datetime.utcnow()
    prescription.dispensed_by = dispense_data.dispensed_by
    prescription.status = "completed"
    
    db.add(prescription)
    db.commit()
    db.refresh(prescription)
    
    log_audit(
        db=db,
        user_id=current_user.id,
        action=AuditAction.DISPENSE_PRESCRIPTION,
        resource_type="prescription",
        resource_id=prescription_id,
        description=f"Dispensed prescription: {prescription_id}, medication: {prescription.medication_name}"
    )
    
    return prescription


@router.delete("/{prescription_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_prescription(
    prescription_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_doctor)
):
    """Delete prescription (doctors and admins only)"""
    prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
    
    if not prescription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prescription not found"
        )
    
    # Only the doctor who created it or admin can delete
    if current_user.id != prescription.doctor_id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this prescription"
        )
    
    db.delete(prescription)
    db.commit()
    
    log_audit(
        db=db,
        user_id=current_user.id,
        action=AuditAction.DELETE,
        resource_type="prescription",
        resource_id=prescription_id,
        description=f"Deleted prescription: {prescription_id}"
    )
