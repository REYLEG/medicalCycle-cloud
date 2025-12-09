"""Consultation tests"""
import pytest
from fastapi import status
from datetime import datetime
from app.models.patient import Patient
from app.models.consultation import Consultation
from app.core.security import create_access_token


@pytest.fixture
def auth_headers(test_doctor):
    """Create authorization headers for test doctor"""
    token = create_access_token(data={"sub": str(test_doctor.id), "role": test_doctor.role.value})
    return {"Authorization": f"Bearer {token}"}


def test_create_consultation(client, test_user, test_doctor, auth_headers, db):
    """Test creating a consultation"""
    # Create patient record
    patient = Patient(user_id=test_user.id)
    db.add(patient)
    db.commit()
    
    response = client.post(
        "/api/v1/consultations/",
        json={
            "patient_id": str(patient.id),
            "doctor_id": str(test_doctor.id),
            "consultation_date": datetime.utcnow().isoformat(),
            "reason": "Routine checkup",
            "chief_complaint": "General checkup",
            "status": "scheduled"
        },
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["patient_id"] == str(patient.id)
    assert data["doctor_id"] == str(test_doctor.id)
    assert data["reason"] == "Routine checkup"


def test_list_consultations(client, test_user, test_doctor, auth_headers, db):
    """Test listing consultations"""
    # Create patient and consultation
    patient = Patient(user_id=test_user.id)
    db.add(patient)
    db.commit()
    
    consultation = Consultation(
        patient_id=patient.id,
        doctor_id=test_doctor.id,
        consultation_date=datetime.utcnow(),
        reason="Checkup"
    )
    db.add(consultation)
    db.commit()
    
    response = client.get(
        "/api/v1/consultations/",
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 1


def test_get_consultation(client, test_user, test_doctor, auth_headers, db):
    """Test getting a specific consultation"""
    # Create patient and consultation
    patient = Patient(user_id=test_user.id)
    db.add(patient)
    db.commit()
    
    consultation = Consultation(
        patient_id=patient.id,
        doctor_id=test_doctor.id,
        consultation_date=datetime.utcnow(),
        diagnosis="Healthy"
    )
    db.add(consultation)
    db.commit()
    
    response = client.get(
        f"/api/v1/consultations/{consultation.id}",
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == str(consultation.id)
    assert data["diagnosis"] == "Healthy"


def test_update_consultation(client, test_user, test_doctor, auth_headers, db):
    """Test updating a consultation"""
    # Create patient and consultation
    patient = Patient(user_id=test_user.id)
    db.add(patient)
    db.commit()
    
    consultation = Consultation(
        patient_id=patient.id,
        doctor_id=test_doctor.id,
        consultation_date=datetime.utcnow(),
        status="in_progress"
    )
    db.add(consultation)
    db.commit()
    
    response = client.put(
        f"/api/v1/consultations/{consultation.id}",
        json={
            "status": "completed",
            "diagnosis": "Patient is healthy",
            "clinical_notes": "All vitals normal"
        },
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "completed"
    assert data["diagnosis"] == "Patient is healthy"


def test_delete_consultation(client, test_user, test_doctor, auth_headers, db):
    """Test deleting a consultation"""
    # Create patient and consultation
    patient = Patient(user_id=test_user.id)
    db.add(patient)
    db.commit()
    
    consultation = Consultation(
        patient_id=patient.id,
        doctor_id=test_doctor.id,
        consultation_date=datetime.utcnow()
    )
    db.add(consultation)
    db.commit()
    
    response = client.delete(
        f"/api/v1/consultations/{consultation.id}",
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
