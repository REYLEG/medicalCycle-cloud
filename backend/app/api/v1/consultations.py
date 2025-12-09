"""Consultation management routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.session import get_db
from app.models.user import User
from app.models.consultation import Consultation
from app.models.patient import Patient
from app.schemas.consultation import ConsultationCreate, ConsultationUpdate, ConsultationResponse
from app.api.deps import get_current_user, get_current_doctor
from app.core.audit import log_audit
from app.models.audit_log import AuditAction

router = APIRouter(prefix="/consultations", tags=["consultations"])


@router.post("/", response_model=ConsultationResponse, status_code=status.HTTP_201_CREATED)
def create_consultation(
    consultation_data: ConsultationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_doctor)
):
    """Create a new consultation (doctors only)"""
    # Verify patient exists
    patient = db.query(Patient).filter(Patient.id == consultation_data.patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    # Verify doctor exists
    doctor = db.query(User).filter(User.id == consultation_data.doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )
    
    consultation = Consultation(**consultation_data.dict())
    db.add(consultation)
    db.commit()
    db.refresh(consultation)
    
    log_audit(
        db=db,
        user_id=current_user.id,
        action=AuditAction.CREATE,
        resource_type="consultation",
        resource_id=consultation.id,
        description=f"Created consultation for patient: {patient.id}"
    )
    
    return consultation


@router.get("/", response_model=list[ConsultationResponse])
def list_consultations(
    patient_id: UUID = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List consultations with optional patient filter"""
    query = db.query(Consultation)
    
    if patient_id:
        query = query.filter(Consultation.patient_id == patient_id)
    
    consultations = query.offset(skip).limit(limit).all()
    
    log_audit(
        db=db,
        user_id=current_user.id,
        action=AuditAction.READ,
        resource_type="consultation",
        description=f"Listed {len(consultations)} consultations"
    )
    
    return consultations


@router.get("/{consultation_id}", response_model=ConsultationResponse)
def get_consultation(
    consultation_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get consultation by ID"""
    consultation = db.query(Consultation).filter(Consultation.id == consultation_id).first()
    
    if not consultation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found"
        )
    
    # Verify access permissions
    patient = consultation.patient
    if (current_user.id != patient.user_id and 
        current_user.id != consultation.doctor_id and 
        current_user.role.value not in ["admin"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this consultation"
        )
    
    log_audit(
        db=db,
        user_id=current_user.id,
        action=AuditAction.READ,
        resource_type="consultation",
        resource_id=consultation_id,
        description=f"Viewed consultation: {consultation_id}"
    )
    
    return consultation


@router.put("/{consultation_id}", response_model=ConsultationResponse)
def update_consultation(
    consultation_id: UUID,
    consultation_data: ConsultationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_doctor)
):
    """Update consultation (doctors only)"""
    consultation = db.query(Consultation).filter(Consultation.id == consultation_id).first()
    
    if not consultation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found"
        )
    
    # Only the doctor who created it or admin can update
    if current_user.id != consultation.doctor_id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this consultation"
        )
    
    update_data = consultation_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(consultation, field, value)
    
    db.add(consultation)
    db.commit()
    db.refresh(consultation)
    
    log_audit(
        db=db,
        user_id=current_user.id,
        action=AuditAction.UPDATE,
        resource_type="consultation",
        resource_id=consultation_id,
        description=f"Updated consultation: {consultation_id}"
    )
    
    return consultation


@router.delete("/{consultation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_consultation(
    consultation_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_doctor)
):
    """Delete consultation (doctors and admins only)"""
    consultation = db.query(Consultation).filter(Consultation.id == consultation_id).first()
    
    if not consultation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found"
        )
    
    # Only the doctor who created it or admin can delete
    if current_user.id != consultation.doctor_id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this consultation"
        )
    
    db.delete(consultation)
    db.commit()
    
    log_audit(
        db=db,
        user_id=current_user.id,
        action=AuditAction.DELETE,
        resource_type="consultation",
        resource_id=consultation_id,
        description=f"Deleted consultation: {consultation_id}"
    )
