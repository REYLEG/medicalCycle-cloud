# MedicalCycle Cloud - Backend API

FastAPI-based backend for the MedicalCycle Cloud medical records management platform.

## Features

- **User Management**: Registration, authentication, role-based access control
- **Patient Records**: Comprehensive patient information management
- **Consultations**: Medical consultation tracking and documentation
- **Prescriptions**: Electronic prescription management with pharmacy integration
- **Audit Logging**: Complete audit trail of all actions
- **Security**: JWT authentication, password hashing, role-based permissions

## Tech Stack

- **Framework**: FastAPI 0.104+
- **Database**: PostgreSQL 14+
- **ORM**: SQLAlchemy 2.0+
- **Authentication**: JWT + OAuth 2.0
- **Validation**: Pydantic 2.0+
- **Server**: Uvicorn

## Installation

### Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Redis 7+ (optional, for caching)

### Local Development Setup

1. **Clone the repository**
```bash
git clone https://github.com/REYLEG/medicalCycle-cloud.git
cd medicalCycle-cloud/backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements-dev.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Start PostgreSQL and Redis**
```bash
# Using Docker
docker-compose up -d postgres redis
```

6. **Run the server**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API Documentation: `http://localhost:8000/api/docs`

### Docker Setup (Recommended)

```bash
cd medicalCycle-cloud
docker-compose up -d
```

This will start:
- PostgreSQL database
- Redis cache
- FastAPI backend

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get access token
- `POST /api/v1/auth/logout` - Logout user
- `GET /api/v1/auth/me` - Get current user info

### Users
- `GET /api/v1/users/` - List all users (admin only)
- `GET /api/v1/users/{user_id}` - Get user by ID
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user (admin only)

### Patients
- `POST /api/v1/patients/` - Create patient record
- `GET /api/v1/patients/` - List patients
- `GET /api/v1/patients/{patient_id}` - Get patient by ID
- `PUT /api/v1/patients/{patient_id}` - Update patient
- `DELETE /api/v1/patients/{patient_id}` - Delete patient

### Consultations
- `POST /api/v1/consultations/` - Create consultation
- `GET /api/v1/consultations/` - List consultations
- `GET /api/v1/consultations/{consultation_id}` - Get consultation
- `PUT /api/v1/consultations/{consultation_id}` - Update consultation
- `DELETE /api/v1/consultations/{consultation_id}` - Delete consultation

### Prescriptions
- `POST /api/v1/prescriptions/` - Create prescription
- `GET /api/v1/prescriptions/` - List prescriptions
- `GET /api/v1/prescriptions/{prescription_id}` - Get prescription
- `PUT /api/v1/prescriptions/{prescription_id}` - Update prescription
- `POST /api/v1/prescriptions/{prescription_id}/dispense` - Dispense prescription
- `DELETE /api/v1/prescriptions/{prescription_id}` - Delete prescription

## User Roles

- **Admin**: Full system access
- **Doctor**: Create consultations and prescriptions
- **Nurse**: View and update patient records and consultations
- **Pharmacist**: View and dispense prescriptions
- **Patient**: View own records and consultations

## Testing

Run tests with pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

## Code Quality

```bash
# Format code
black app/

# Lint
flake8 app/

# Type checking
mypy app/

# Sort imports
isort app/
```

## Environment Variables

See `.env.example` for all available configuration options:

- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT secret key (change in production!)
- `ALGORITHM` - JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time
- `ALLOWED_ORIGINS` - CORS allowed origins
- `ENVIRONMENT` - Environment (development/production)
- `DEBUG` - Debug mode (true/false)

## Security

- Passwords are hashed with bcrypt
- JWT tokens for authentication
- Role-based access control (RBAC)
- Complete audit logging
- CORS protection
- SQL injection prevention via SQLAlchemy ORM

## Database Schema

### Users
- id (UUID)
- email (unique)
- username (unique)
- full_name
- hashed_password
- role (admin, doctor, nurse, pharmacist, patient)
- is_active
- is_verified
- phone
- license_number (for healthcare professionals)

### Patients
- id (UUID)
- user_id (foreign key)
- date_of_birth
- gender
- blood_type
- address, city, postal_code, country
- emergency_contact_name, emergency_contact_phone
- allergies
- chronic_conditions
- family_history
- insurance_number, insurance_provider

### Consultations
- id (UUID)
- patient_id (foreign key)
- doctor_id (foreign key)
- consultation_date
- status (scheduled, in_progress, completed, cancelled)
- reason, chief_complaint
- diagnosis, clinical_notes
- vital_signs, physical_examination
- treatment_plan
- follow_up_date

### Prescriptions
- id (UUID)
- patient_id (foreign key)
- doctor_id (foreign key)
- consultation_id (foreign key, optional)
- medication_name
- dosage, frequency, duration, route
- quantity, refills
- status (active, completed, cancelled, expired)
- prescribed_date, expiry_date
- dispensed_date, dispensed_by

### Audit Logs
- id (UUID)
- user_id (foreign key)
- action (create, read, update, delete, login, logout)
- resource_type
- resource_id
- timestamp

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions, please open an issue on GitHub.
