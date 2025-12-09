# MedicalCycle Cloud - Architecture Documentation

## System Overview

MedicalCycle Cloud is a secure, scalable medical records management platform built with modern cloud-native technologies.

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client Layer                              │
│                    (React Frontend)                              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                    HTTPS / TLS 1.3
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                      API Gateway                                 │
│                   (Load Balancer)                                │
└────────────────────────────┬────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼────────┐
│   FastAPI      │  │   FastAPI       │  │   FastAPI     │
│   Instance 1   │  │   Instance 2    │  │   Instance N  │
│                │  │                 │  │               │
│ ┌────────────┐ │  │ ┌────────────┐  │  │ ┌──────────┐ │
│ │ Auth       │ │  │ │ Auth       │  │  │ │ Auth     │ │
│ │ Routes     │ │  │ │ Routes     │  │  │ │ Routes   │ │
│ └────────────┘ │  │ └────────────┘  │  │ └──────────┘ │
│ ┌────────────┐ │  │ ┌────────────┐  │  │ ┌──────────┐ │
│ │ Patient    │ │  │ │ Patient    │  │  │ │ Patient  │ │
│ │ Routes     │ │  │ │ Routes     │  │  │ │ Routes   │ │
│ └────────────┘ │  │ └────────────┘  │  │ └──────────┘ │
│ ┌────────────┐ │  │ ┌────────────┐  │  │ ┌──────────┐ │
│ │ Consult.   │ │  │ │ Consult.   │  │  │ │ Consult. │ │
│ │ Routes     │ │  │ │ Routes     │  │  │ │ Routes   │ │
│ └────────────┘ │  │ └────────────┘  │  │ └──────────┘ │
│ ┌────────────┐ │  │ ┌────────────┐  │  │ ┌──────────┐ │
│ │ Prescrip.  │ │  │ │ Prescrip.  │  │  │ │ Prescrip.│ │
│ │ Routes     │ │  │ │ Routes     │  │  │ │ Routes   │ │
│ └────────────┘ │  │ └────────────┘  │  │ └──────────┘ │
└────────────────┘  └─────────────────┘  └──────────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼──────────┐  ┌──────▼──────────┐  ┌────▼────────────┐
│   PostgreSQL     │  │   Redis Cache   │  │  Audit Logs     │
│   (Master)       │  │                 │  │  (PostgreSQL)   │
│                  │  │ - Sessions      │  │                 │
│ - Users          │  │ - Cache         │  │ - All Actions   │
│ - Patients       │  │ - Rate Limits   │  │ - Timestamps    │
│ - Consultations  │  │                 │  │ - User Info     │
│ - Prescriptions  │  │                 │  │                 │
└────────┬─────────┘  └─────────────────┘  └─────────────────┘
         │
         │ Replication
         │
┌────────▼──────────┐
│   PostgreSQL      │
│   (Slave)         │
│   Read-Only       │
└───────────────────┘
```

## Backend Architecture

### Layered Architecture

```
┌─────────────────────────────────────────┐
│         API Layer (Routes)              │
│  auth.py, users.py, patients.py, etc.  │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│    Business Logic Layer (Services)      │
│  patient_service.py, etc.               │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│      Data Access Layer (Models)         │
│  SQLAlchemy ORM Models                  │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│      Database Layer                     │
│  PostgreSQL / Redis                     │
└─────────────────────────────────────────┘
```

### Directory Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Configuration management
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py             # Dependency injection
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py         # Authentication routes
│   │       ├── users.py        # User management routes
│   │       ├── patients.py     # Patient routes
│   │       ├── consultations.py # Consultation routes
│   │       └── prescriptions.py # Prescription routes
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py         # JWT, password hashing
│   │   ├── permissions.py      # RBAC logic
│   │   └── audit.py            # Audit logging
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py             # User model
│   │   ├── patient.py          # Patient model
│   │   ├── consultation.py     # Consultation model
│   │   ├── prescription.py     # Prescription model
│   │   └── audit_log.py        # Audit log model
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py             # User schemas (Pydantic)
│   │   ├── patient.py          # Patient schemas
│   │   ├── consultation.py     # Consultation schemas
│   │   └── prescription.py     # Prescription schemas
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py             # SQLAlchemy Base
│   │   ├── session.py          # Database session
│   │   └── init_db.py          # DB initialization
│   │
│   └── services/               # Business logic (future)
│       └── __init__.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Test fixtures
│   ├── test_auth.py
│   ├── test_patients.py
│   ├── test_consultations.py
│   └── test_prescriptions.py
│
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
├── .env.example
├── .gitignore
├── pytest.ini
├── pyproject.toml
└── README.md
```

## Data Models

### User Model
- Represents healthcare professionals and patients
- Roles: Admin, Doctor, Nurse, Pharmacist, Patient
- Stores authentication credentials (hashed)
- Tracks professional licenses

### Patient Model
- Linked to User model (one-to-one)
- Stores medical history
- Emergency contact information
- Insurance details
- Allergies and chronic conditions

### Consultation Model
- Represents a medical visit
- Links Patient and Doctor
- Stores clinical notes, diagnosis, treatment plan
- Tracks consultation status

### Prescription Model
- Represents medication prescription
- Links to Patient and Doctor
- Tracks dispensing status
- Supports refills

### Audit Log Model
- Immutable record of all actions
- Tracks who did what, when, and where
- Supports compliance and security audits

## Security Architecture

### Authentication Flow

```
1. User Registration
   ├── Email validation
   ├── Password hashing (bcrypt)
   └── User created in database

2. User Login
   ├── Email/password verification
   ├── JWT token generation
   └── Token returned to client

3. API Request
   ├── Client sends token in Authorization header
   ├── Token validation and decoding
   ├── User identity verification
   ├── Permission check
   └── Request processed or rejected

4. Token Expiration
   ├── Default: 30 minutes
   ├── Automatic refresh (future)
   └── User re-authentication required
```

### Authorization (RBAC)

| Role | Permissions |
|------|------------|
| Admin | All operations |
| Doctor | Create/read consultations, prescriptions |
| Nurse | Read/update patient records, consultations |
| Pharmacist | Read prescriptions, dispense medications |
| Patient | Read own records and consultations |

### Data Protection

- **In Transit**: TLS 1.3 encryption
- **At Rest**: AES-256 encryption (future)
- **Hashing**: bcrypt for passwords
- **Tokenization**: JWT for sessions
- **Audit Trail**: All actions logged

## API Design

### RESTful Principles

- Resource-based URLs
- Standard HTTP methods (GET, POST, PUT, DELETE)
- Consistent response formats
- Proper HTTP status codes

### Response Format

```json
{
  "id": "uuid",
  "email": "user@example.com",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### Error Handling

```json
{
  "detail": "Error message"
}
```

## Deployment Architecture

### Development
- Single instance
- SQLite or local PostgreSQL
- Hot reload enabled

### Production
- Multiple FastAPI instances (auto-scaling)
- Load balancer (AWS ALB, GCP LB, etc.)
- PostgreSQL with replication
- Redis for caching
- CDN for static assets
- WAF protection
- DDoS protection

## Performance Considerations

- Connection pooling (SQLAlchemy)
- Query optimization with indexes
- Redis caching for frequently accessed data
- Pagination for list endpoints
- Async operations (future)

## Monitoring & Logging

- Application logs (stdout/stderr)
- Audit logs (database)
- Performance metrics (Prometheus, future)
- Error tracking (Sentry, future)
- Health checks (/health endpoint)

## Future Enhancements

- Microservices architecture
- Message queues (Celery, RabbitMQ)
- GraphQL API
- Real-time notifications (WebSockets)
- Advanced analytics
- Machine learning integration
- Mobile app API
