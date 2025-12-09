"""Patient management routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.session import get_db
from app.models.user import User
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate, PatientResponse
from app.api.deps import get_current_user, get_current_doctor
from app.core.audit import log_audit
from app.models.audit_log import AuditAction

router = APIRouter(prefix="/patients", tags=["patients"])


@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(
    patient_data: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new patient record"""
    # Check if user exists
    user = db.query(User).filter(User.id == patient_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if patient already exists for this user
    existing_patient = db.query(Patient).filter(Patient.user_id == patient_data.user_id).first()
    if existing_patient:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Patient record already exists for this user"
        )
    
    patient = Patient(**patient_data.dict())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    
    log_audit(
        db=db,
        user_id=current_user.id,
        action=AuditAction.CREATE,
        resource_type="patient",
        resource_id=patient.id,
        description=f"Created patient record for user: {user.email}"
    )
    
    return patient


@router.get("/", response_model=list[PatientResponse])
def list_patients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_doctor)
):
    """List all patients (doctors and admins only)"""
    patients = db.query(Patient).offset(skip).limit(limit).all()
    
    log_audit(
        db=db,
        user_id=current_user.id,
        action=AuditAction.READ,
        resource_type="patient",
        description=f"Listed {len(patients)} patients"
    )
    
    return patients


@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(
    patient_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get patient by ID"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    # Patients can only view their own record unless they are doctor/admin
    if current_user.id != patient.user_id and current_user.role.value not in ["doctor", "nurse", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this patient record"
        )
    
    log_audit(
        db=db,
        user_id=current_user.id,
        action=AuditAction.READ,
        resource_type="patient",
        resource_id=patient_id,
        description=f"Viewed patient record: {patient_id}"
    )
    
    return patient


@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(
    patient_id: UUID,
    patient_data: PatientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update patient information"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    # Patients can only update their own record unless they are doctor/admin
    if current_user.id != patient.user_id and current_user.role.value not in ["doctor", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this patient record"
        )
    
    update_data = patient_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(patient, field, value)
    
    db.add(patient)
    db.commit()
    db.refresh(patient)
    
    log_audit(
        db=db,
        user_id=current_user.id,
        action=AuditAction.UPDATE,
        resource_type="patient",
        resource_id=patient_id,
        description=f"Updated patient record: {patient_id}"
    )
    
    return patient


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(
    patient_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_doctor)
):
    """Delete patient record (doctors and admins only)"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    db.delete(patient)
    db.commit()
    
    log_audit(
        db=db,
        user_id=current_user.id,
        action=AuditAction.DELETE,
        resource_type="patient",
        resource_id=patient_id,
        description=f"Deleted patient record: {patient_id}"
    )
