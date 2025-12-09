# MedicalCycle Cloud - API Documentation

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

All endpoints (except `/auth/register` and `/auth/login`) require a Bearer token in the Authorization header:

```
Authorization: Bearer <access_token>
```

## Response Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `204 No Content` - Request successful, no content to return
- `400 Bad Request` - Invalid request parameters
- `401 Unauthorized` - Missing or invalid authentication
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Authentication Endpoints

### Register User

**POST** `/auth/register`

Create a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "password": "securepassword123",
  "role": "patient",
  "phone": "+1234567890",
  "license_number": null
}
```

**Response (201):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "role": "patient",
  "is_active": true,
  "is_verified": false,
  "phone": "+1234567890",
  "license_number": null,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00",
  "last_login": null
}
```

### Login

**POST** `/auth/login`

Authenticate user and get access token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Logout

**POST** `/auth/logout`

Logout current user.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "message": "Successfully logged out"
}
```

### Get Current User

**GET** `/auth/me`

Get information about the currently authenticated user.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "role": "patient",
  "is_active": true,
  "is_verified": true,
  "phone": "+1234567890",
  "license_number": null,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00",
  "last_login": "2024-01-01T10:00:00"
}
```

## User Management Endpoints

### List Users

**GET** `/users/`

List all users (Admin only).

**Query Parameters:**
- `skip` (int, default: 0) - Number of records to skip
- `limit` (int, default: 100) - Maximum records to return

**Headers:**
```
Authorization: Bearer <admin_token>
```

**Response (200):**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "username": "username",
    "full_name": "Full Name",
    "role": "patient",
    "is_active": true,
    "is_verified": true,
    "phone": "+1234567890",
    "license_number": null,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00",
    "last_login": "2024-01-01T10:00:00"
  }
]
```

### Get User

**GET** `/users/{user_id}`

Get user by ID.

**Path Parameters:**
- `user_id` (UUID) - User ID

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "role": "patient",
  "is_active": true,
  "is_verified": true,
  "phone": "+1234567890",
  "license_number": null,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00",
  "last_login": "2024-01-01T10:00:00"
}
```

### Update User

**PUT** `/users/{user_id}`

Update user information.

**Path Parameters:**
- `user_id` (UUID) - User ID

**Request Body:**
```json
{
  "email": "newemail@example.com",
  "username": "newusername",
  "full_name": "New Full Name",
  "phone": "+9876543210",
  "license_number": null
}
```

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "newemail@example.com",
  "username": "newusername",
  "full_name": "New Full Name",
  "role": "patient",
  "is_active": true,
  "is_verified": true,
  "phone": "+9876543210",
  "license_number": null,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T12:00:00",
  "last_login": "2024-01-01T10:00:00"
}
```

### Delete User

**DELETE** `/users/{user_id}`

Delete user (Admin only).

**Path Parameters:**
- `user_id` (UUID) - User ID

**Headers:**
```
Authorization: Bearer <admin_token>
```

**Response (204):** No content

## Patient Endpoints

### Create Patient

**POST** `/patients/`

Create a new patient record.

**Request Body:**
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "date_of_birth": "1990-01-15T00:00:00",
  "gender": "M",
  "blood_type": "O+",
  "address": "123 Main Street",
  "city": "New York",
  "postal_code": "10001",
  "country": "USA",
  "emergency_contact_name": "Jane Doe",
  "emergency_contact_phone": "+1234567890",
  "allergies": "Penicillin, Sulfa drugs",
  "chronic_conditions": "Diabetes Type 2",
  "family_history": "Hypertension",
  "insurance_number": "INS123456",
  "insurance_provider": "Blue Cross"
}
```

**Response (201):**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "date_of_birth": "1990-01-15T00:00:00",
  "gender": "M",
  "blood_type": "O+",
  "address": "123 Main Street",
  "city": "New York",
  "postal_code": "10001",
  "country": "USA",
  "emergency_contact_name": "Jane Doe",
  "emergency_contact_phone": "+1234567890",
  "allergies": "Penicillin, Sulfa drugs",
  "chronic_conditions": "Diabetes Type 2",
  "family_history": "Hypertension",
  "insurance_number": "INS123456",
  "insurance_provider": "Blue Cross",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### List Patients

**GET** `/patients/`

List all patients (Doctors and Admins only).

**Query Parameters:**
- `skip` (int, default: 0) - Number of records to skip
- `limit` (int, default: 100) - Maximum records to return

**Response (200):**
```json
[
  {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "date_of_birth": "1990-01-15T00:00:00",
    "gender": "M",
    "blood_type": "O+",
    "address": "123 Main Street",
    "city": "New York",
    "postal_code": "10001",
    "country": "USA",
    "emergency_contact_name": "Jane Doe",
    "emergency_contact_phone": "+1234567890",
    "allergies": "Penicillin, Sulfa drugs",
    "chronic_conditions": "Diabetes Type 2",
    "family_history": "Hypertension",
    "insurance_number": "INS123456",
    "insurance_provider": "Blue Cross",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
]
```

### Get Patient

**GET** `/patients/{patient_id}`

Get patient by ID.

**Path Parameters:**
- `patient_id` (UUID) - Patient ID

**Response (200):**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "date_of_birth": "1990-01-15T00:00:00",
  "gender": "M",
  "blood_type": "O+",
  "address": "123 Main Street",
  "city": "New York",
  "postal_code": "10001",
  "country": "USA",
  "emergency_contact_name": "Jane Doe",
  "emergency_contact_phone": "+1234567890",
  "allergies": "Penicillin, Sulfa drugs",
  "chronic_conditions": "Diabetes Type 2",
  "family_history": "Hypertension",
  "insurance_number": "INS123456",
  "insurance_provider": "Blue Cross",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### Update Patient

**PUT** `/patients/{patient_id}`

Update patient information.

**Path Parameters:**
- `patient_id` (UUID) - Patient ID

**Request Body:**
```json
{
  "gender": "F",
  "blood_type": "A+",
  "allergies": "Penicillin, Sulfa drugs, Aspirin",
  "chronic_conditions": "Diabetes Type 2, Hypertension"
}
```

**Response (200):**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "date_of_birth": "1990-01-15T00:00:00",
  "gender": "F",
  "blood_type": "A+",
  "address": "123 Main Street",
  "city": "New York",
  "postal_code": "10001",
  "country": "USA",
  "emergency_contact_name": "Jane Doe",
  "emergency_contact_phone": "+1234567890",
  "allergies": "Penicillin, Sulfa drugs, Aspirin",
  "chronic_conditions": "Diabetes Type 2, Hypertension",
  "family_history": "Hypertension",
  "insurance_number": "INS123456",
  "insurance_provider": "Blue Cross",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T12:00:00"
}
```

### Delete Patient

**DELETE** `/patients/{patient_id}`

Delete patient record (Doctors and Admins only).

**Path Parameters:**
- `patient_id` (UUID) - Patient ID

**Response (204):** No content

## Consultation Endpoints

### Create Consultation

**POST** `/consultations/`

Create a new consultation (Doctors only).

**Request Body:**
```json
{
  "patient_id": "660e8400-e29b-41d4-a716-446655440001",
  "doctor_id": "770e8400-e29b-41d4-a716-446655440002",
  "consultation_date": "2024-01-15T14:30:00",
  "reason": "Follow-up for diabetes",
  "chief_complaint": "Blood sugar control",
  "status": "scheduled"
}
```

**Response (201):**
```json
{
  "id": "880e8400-e29b-41d4-a716-446655440003",
  "patient_id": "660e8400-e29b-41d4-a716-446655440001",
  "doctor_id": "770e8400-e29b-41d4-a716-446655440002",
  "consultation_date": "2024-01-15T14:30:00",
  "status": "scheduled",
  "reason": "Follow-up for diabetes",
  "chief_complaint": "Blood sugar control",
  "diagnosis": null,
  "clinical_notes": null,
  "vital_signs": null,
  "physical_examination": null,
  "treatment_plan": null,
  "follow_up_date": null,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### List Consultations

**GET** `/consultations/`

List consultations with optional filters.

**Query Parameters:**
- `patient_id` (UUID, optional) - Filter by patient
- `skip` (int, default: 0) - Number of records to skip
- `limit` (int, default: 100) - Maximum records to return

**Response (200):**
```json
[
  {
    "id": "880e8400-e29b-41d4-a716-446655440003",
    "patient_id": "660e8400-e29b-41d4-a716-446655440001",
    "doctor_id": "770e8400-e29b-41d4-a716-446655440002",
    "consultation_date": "2024-01-15T14:30:00",
    "status": "scheduled",
    "reason": "Follow-up for diabetes",
    "chief_complaint": "Blood sugar control",
    "diagnosis": null,
    "clinical_notes": null,
    "vital_signs": null,
    "physical_examination": null,
    "treatment_plan": null,
    "follow_up_date": null,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
]
```

### Get Consultation

**GET** `/consultations/{consultation_id}`

Get consultation by ID.

**Path Parameters:**
- `consultation_id` (UUID) - Consultation ID

**Response (200):**
```json
{
  "id": "880e8400-e29b-41d4-a716-446655440003",
  "patient_id": "660e8400-e29b-41d4-a716-446655440001",
  "doctor_id": "770e8400-e29b-41d4-a716-446655440002",
  "consultation_date": "2024-01-15T14:30:00",
  "status": "completed",
  "reason": "Follow-up for diabetes",
  "chief_complaint": "Blood sugar control",
  "diagnosis": "Diabetes well controlled",
  "clinical_notes": "Patient shows good compliance",
  "vital_signs": "{\"bp\": \"120/80\", \"hr\": 72}",
  "physical_examination": "Normal",
  "treatment_plan": "Continue current medication",
  "follow_up_date": "2024-02-15T14:30:00",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-15T15:00:00"
}
```

### Update Consultation

**PUT** `/consultations/{consultation_id}`

Update consultation (Doctors only).

**Path Parameters:**
- `consultation_id` (UUID) - Consultation ID

**Request Body:**
```json
{
  "status": "completed",
  "diagnosis": "Diabetes well controlled",
  "clinical_notes": "Patient shows good compliance",
  "vital_signs": "{\"bp\": \"120/80\", \"hr\": 72}",
  "physical_examination": "Normal",
  "treatment_plan": "Continue current medication",
  "follow_up_date": "2024-02-15T14:30:00"
}
```

**Response (200):**
```json
{
  "id": "880e8400-e29b-41d4-a716-446655440003",
  "patient_id": "660e8400-e29b-41d4-a716-446655440001",
  "doctor_id": "770e8400-e29b-41d4-a716-446655440002",
  "consultation_date": "2024-01-15T14:30:00",
  "status": "completed",
  "reason": "Follow-up for diabetes",
  "chief_complaint": "Blood sugar control",
  "diagnosis": "Diabetes well controlled",
  "clinical_notes": "Patient shows good compliance",
  "vital_signs": "{\"bp\": \"120/80\", \"hr\": 72}",
  "physical_examination": "Normal",
  "treatment_plan": "Continue current medication",
  "follow_up_date": "2024-02-15T14:30:00",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-15T15:00:00"
}
```

### Delete Consultation

**DELETE** `/consultations/{consultation_id}`

Delete consultation (Doctors and Admins only).

**Path Parameters:**
- `consultation_id` (UUID) - Consultation ID

**Response (204):** No content

## Prescription Endpoints

### Create Prescription

**POST** `/prescriptions/`

Create a new prescription (Doctors only).

**Request Body:**
```json
{
  "patient_id": "660e8400-e29b-41d4-a716-446655440001",
  "doctor_id": "770e8400-e29b-41d4-a716-446655440002",
  "consultation_id": "880e8400-e29b-41d4-a716-446655440003",
  "medication_name": "Metformin",
  "dosage": "500mg",
  "frequency": "2 times daily",
  "duration": "30 days",
  "route": "oral",
  "quantity": 60,
  "refills": 2,
  "notes": "Take with meals",
  "contraindications": "Renal impairment",
  "side_effects": "Nausea, diarrhea"
}
```

**Response (201):**
```json
{
  "id": "990e8400-e29b-41d4-a716-446655440004",
  "patient_id": "660e8400-e29b-41d4-a716-446655440001",
  "doctor_id": "770e8400-e29b-41d4-a716-446655440002",
  "consultation_id": "880e8400-e29b-41d4-a716-446655440003",
  "medication_name": "Metformin",
  "dosage": "500mg",
  "frequency": "2 times daily",
  "duration": "30 days",
  "route": "oral",
  "quantity": 60,
  "refills": 2,
  "status": "active",
  "notes": "Take with meals",
  "contraindications": "Renal impairment",
  "side_effects": "Nausea, diarrhea",
  "prescribed_date": "2024-01-15T15:00:00",
  "expiry_date": null,
  "dispensed_date": null,
  "dispensed_by": null,
  "created_at": "2024-01-15T15:00:00",
  "updated_at": "2024-01-15T15:00:00"
}
```

### List Prescriptions

**GET** `/prescriptions/`

List prescriptions with optional filters.

**Query Parameters:**
- `patient_id` (UUID, optional) - Filter by patient
- `status_filter` (string, optional) - Filter by status (active, completed, cancelled, expired)
- `skip` (int, default: 0) - Number of records to skip
- `limit` (int, default: 100) - Maximum records to return

**Response (200):**
```json
[
  {
    "id": "990e8400-e29b-41d4-a716-446655440004",
    "patient_id": "660e8400-e29b-41d4-a716-446655440001",
    "doctor_id": "770e8400-e29b-41d4-a716-446655440002",
    "consultation_id": "880e8400-e29b-41d4-a716-446655440003",
    "medication_name": "Metformin",
    "dosage": "500mg",
    "frequency": "2 times daily",
    "duration": "30 days",
    "route": "oral",
    "quantity": 60,
    "refills": 2,
    "status": "active",
    "notes": "Take with meals",
    "contraindications": "Renal impairment",
    "side_effects": "Nausea, diarrhea",
    "prescribed_date": "2024-01-15T15:00:00",
    "expiry_date": null,
    "dispensed_date": null,
    "dispensed_by": null,
    "created_at": "2024-01-15T15:00:00",
    "updated_at": "2024-01-15T15:00:00"
  }
]
```

### Get Prescription

**GET** `/prescriptions/{prescription_id}`

Get prescription by ID.

**Path Parameters:**
- `prescription_id` (UUID) - Prescription ID

**Response (200):**
```json
{
  "id": "990e8400-e29b-41d4-a716-446655440004",
  "patient_id": "660e8400-e29b-41d4-a716-446655440001",
  "doctor_id": "770e8400-e29b-41d4-a716-446655440002",
  "consultation_id": "880e8400-e29b-41d4-a716-446655440003",
  "medication_name": "Metformin",
  "dosage": "500mg",
  "frequency": "2 times daily",
  "duration": "30 days",
  "route": "oral",
  "quantity": 60,
  "refills": 2,
  "status": "completed",
  "notes": "Take with meals",
  "contraindications": "Renal impairment",
  "side_effects": "Nausea, diarrhea",
  "prescribed_date": "2024-01-15T15:00:00",
  "expiry_date": null,
  "dispensed_date": "2024-01-16T10:00:00",
  "dispensed_by": "aa0e8400-e29b-41d4-a716-446655440005",
  "created_at": "2024-01-15T15:00:00",
  "updated_at": "2024-01-16T10:00:00"
}
```

### Update Prescription

**PUT** `/prescriptions/{prescription_id}`

Update prescription (Doctors only).

**Path Parameters:**
- `prescription_id` (UUID) - Prescription ID

**Request Body:**
```json
{
  "status": "completed",
  "refills": 1,
  "notes": "Patient tolerating well"
}
```

**Response (200):**
```json
{
  "id": "990e8400-e29b-41d4-a716-446655440004",
  "patient_id": "660e8400-e29b-41d4-a716-446655440001",
  "doctor_id": "770e8400-e29b-41d4-a716-446655440002",
  "consultation_id": "880e8400-e29b-41d4-a716-446655440003",
  "medication_name": "Metformin",
  "dosage": "500mg",
  "frequency": "2 times daily",
  "duration": "30 days",
  "route": "oral",
  "quantity": 60,
  "refills": 1,
  "status": "completed",
  "notes": "Patient tolerating well",
  "contraindications": "Renal impairment",
  "side_effects": "Nausea, diarrhea",
  "prescribed_date": "2024-01-15T15:00:00",
  "expiry_date": null,
  "dispensed_date": "2024-01-16T10:00:00",
  "dispensed_by": "aa0e8400-e29b-41d4-a716-446655440005",
  "created_at": "2024-01-15T15:00:00",
  "updated_at": "2024-01-16T12:00:00"
}
```

### Dispense Prescription

**POST** `/prescriptions/{prescription_id}/dispense`

Dispense prescription (Pharmacists only).

**Path Parameters:**
- `prescription_id` (UUID) - Prescription ID

**Request Body:**
```json
{
  "dispensed_by": "aa0e8400-e29b-41d4-a716-446655440005"
}
```

**Response (200):**
```json
{
  "id": "990e8400-e29b-41d4-a716-446655440004",
  "patient_id": "660e8400-e29b-41d4-a716-446655440001",
  "doctor_id": "770e8400-e29b-41d4-a716-446655440002",
  "consultation_id": "880e8400-e29b-41d4-a716-446655440003",
  "medication_name": "Metformin",
  "dosage": "500mg",
  "frequency": "2 times daily",
  "duration": "30 days",
  "route": "oral",
  "quantity": 60,
  "refills": 2,
  "status": "completed",
  "notes": "Take with meals",
  "contraindications": "Renal impairment",
  "side_effects": "Nausea, diarrhea",
  "prescribed_date": "2024-01-15T15:00:00",
  "expiry_date": null,
  "dispensed_date": "2024-01-16T10:00:00",
  "dispensed_by": "aa0e8400-e29b-41d4-a716-446655440005",
  "created_at": "2024-01-15T15:00:00",
  "updated_at": "2024-01-16T10:00:00"
}
```

### Delete Prescription

**DELETE** `/prescriptions/{prescription_id}`

Delete prescription (Doctors and Admins only).

**Path Parameters:**
- `prescription_id` (UUID) - Prescription ID

**Response (204):** No content

## Error Examples

### 401 Unauthorized
```json
{
  "detail": "Invalid authentication credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Not authorized to view this patient record"
}
```

### 404 Not Found
```json
{
  "detail": "Patient not found"
}
```

### 400 Bad Request
```json
{
  "detail": "Email or username already registered"
}
```

## Rate Limiting

Currently not implemented. Will be added in future versions.

## Pagination

List endpoints support pagination via `skip` and `limit` query parameters.

Example:
```
GET /api/v1/patients/?skip=0&limit=10
```

## Filtering

Some list endpoints support filtering:

- Consultations: Filter by `patient_id`
- Prescriptions: Filter by `patient_id` and `status_filter`

## Sorting

Sorting is not currently implemented. Will be added in future versions.
