"""Patient tests"""
import pytest
from fastapi import status
from app.models.patient import Patient
from app.core.security import create_access_token


@pytest.fixture
def auth_headers(test_doctor):
    """Create authorization headers for test doctor"""
    token = create_access_token(data={"sub": str(test_doctor.id), "role": test_doctor.role.value})
    return {"Authorization": f"Bearer {token}"}


def test_create_patient(client, test_user, auth_headers):
    """Test creating a patient record"""
    response = client.post(
        "/api/v1/patients/",
        json={
            "user_id": str(test_user.id),
            "date_of_birth": "1990-01-01T00:00:00",
            "gender": "M",
            "blood_type": "O+",
            "address": "123 Main St",
            "city": "New York",
            "postal_code": "10001",
            "country": "USA",
            "allergies": "Penicillin",
            "chronic_conditions": "Diabetes"
        },
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["user_id"] == str(test_user.id)
    assert data["blood_type"] == "O+"


def test_create_patient_duplicate(client, test_user, auth_headers, db):
    """Test creating duplicate patient record"""
    # Create first patient
    patient = Patient(user_id=test_user.id)
    db.add(patient)
    db.commit()
    
    # Try to create another
    response = client.post(
        "/api/v1/patients/",
        json={
            "user_id": str(test_user.id),
            "gender": "M"
        },
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_list_patients(client, test_user, test_doctor, auth_headers, db):
    """Test listing patients"""
    # Create patient record
    patient = Patient(user_id=test_user.id, gender="M")
    db.add(patient)
    db.commit()
    
    response = client.get(
        "/api/v1/patients/",
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 1


def test_get_patient(client, test_user, test_doctor, auth_headers, db):
    """Test getting a specific patient"""
    # Create patient record
    patient = Patient(user_id=test_user.id, gender="M", blood_type="A+")
    db.add(patient)
    db.commit()
    
    response = client.get(
        f"/api/v1/patients/{patient.id}",
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == str(patient.id)
    assert data["blood_type"] == "A+"


def test_get_patient_not_found(client, auth_headers):
    """Test getting nonexistent patient"""
    response = client.get(
        "/api/v1/patients/00000000-0000-0000-0000-000000000000",
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_patient(client, test_user, test_doctor, auth_headers, db):
    """Test updating patient information"""
    # Create patient record
    patient = Patient(user_id=test_user.id, gender="M")
    db.add(patient)
    db.commit()
    
    response = client.put(
        f"/api/v1/patients/{patient.id}",
        json={
            "gender": "F",
            "blood_type": "B-",
            "allergies": "Aspirin"
        },
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["gender"] == "F"
    assert data["blood_type"] == "B-"
    assert data["allergies"] == "Aspirin"


def test_delete_patient(client, test_user, test_doctor, auth_headers, db):
    """Test deleting a patient"""
    # Create patient record
    patient = Patient(user_id=test_user.id)
    db.add(patient)
    db.commit()
    
    response = client.delete(
        f"/api/v1/patients/{patient.id}",
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
