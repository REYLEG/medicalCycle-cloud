"""Prescription tests"""
import pytest
from fastapi import status
from datetime import datetime
from app.models.patient import Patient
from app.models.prescription import Prescription
from app.core.security import create_access_token


@pytest.fixture
def auth_headers(test_doctor):
    """Create authorization headers for test doctor"""
    token = create_access_token(data={"sub": str(test_doctor.id), "role": test_doctor.role.value})
    return {"Authorization": f"Bearer {token}"}


def test_create_prescription(client, test_user, test_doctor, auth_headers, db):
    """Test creating a prescription"""
    # Create patient record
    patient = Patient(user_id=test_user.id)
    db.add(patient)
    db.commit()
    
    response = client.post(
        "/api/v1/prescriptions/",
        json={
            "patient_id": str(patient.id),
            "doctor_id": str(test_doctor.id),
            "medication_name": "Aspirin",
            "dosage": "500mg",
            "frequency": "2 times daily",
            "duration": "7 days",
            "route": "oral",
            "quantity": 14,
            "refills": 0
        },
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["medication_name"] == "Aspirin"
    assert data["dosage"] == "500mg"
    assert data["status"] == "active"


def test_list_prescriptions(client, test_user, test_doctor, auth_headers, db):
    """Test listing prescriptions"""
    # Create patient and prescription
    patient = Patient(user_id=test_user.id)
    db.add(patient)
    db.commit()
    
    prescription = Prescription(
        patient_id=patient.id,
        doctor_id=test_doctor.id,
        medication_name="Ibuprofen",
        dosage="200mg",
        frequency="3 times daily",
        duration="5 days",
        route="oral"
    )
    db.add(prescription)
    db.commit()
    
    response = client.get(
        "/api/v1/prescriptions/",
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 1


def test_get_prescription(client, test_user, test_doctor, auth_headers, db):
    """Test getting a specific prescription"""
    # Create patient and prescription
    patient = Patient(user_id=test_user.id)
    db.add(patient)
    db.commit()
    
    prescription = Prescription(
        patient_id=patient.id,
        doctor_id=test_doctor.id,
        medication_name="Metformin",
        dosage="500mg",
        frequency="2 times daily",
        duration="30 days",
        route="oral"
    )
    db.add(prescription)
    db.commit()
    
    response = client.get(
        f"/api/v1/prescriptions/{prescription.id}",
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == str(prescription.id)
    assert data["medication_name"] == "Metformin"


def test_update_prescription(client, test_user, test_doctor, auth_headers, db):
    """Test updating a prescription"""
    # Create patient and prescription
    patient = Patient(user_id=test_user.id)
    db.add(patient)
    db.commit()
    
    prescription = Prescription(
        patient_id=patient.id,
        doctor_id=test_doctor.id,
        medication_name="Lisinopril",
        dosage="10mg",
        frequency="1 time daily",
        duration="30 days",
        route="oral"
    )
    db.add(prescription)
    db.commit()
    
    response = client.put(
        f"/api/v1/prescriptions/{prescription.id}",
        json={
            "status": "completed",
            "refills": 2
        },
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["refills"] == 2


def test_delete_prescription(client, test_user, test_doctor, auth_headers, db):
    """Test deleting a prescription"""
    # Create patient and prescription
    patient = Patient(user_id=test_user.id)
    db.add(patient)
    db.commit()
    
    prescription = Prescription(
        patient_id=patient.id,
        doctor_id=test_doctor.id,
        medication_name="Amoxicillin",
        dosage="250mg",
        frequency="3 times daily",
        duration="10 days",
        route="oral"
    )
    db.add(prescription)
    db.commit()
    
    response = client.delete(
        f"/api/v1/prescriptions/{prescription.id}",
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
