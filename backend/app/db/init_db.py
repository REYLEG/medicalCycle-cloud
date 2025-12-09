"""Database initialization script"""
from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.models.user import User, UserRole
from app.core.security import hash_password


def init_db():
    """Initialize database with tables and sample data"""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if admin user exists
        admin_user = db.query(User).filter(User.email == "admin@medicalcycle.local").first()
        
        if not admin_user:
            # Create admin user
            admin = User(
                email="admin@medicalcycle.local",
                username="admin",
                full_name="System Administrator",
                hashed_password=hash_password("admin123"),
                role=UserRole.ADMIN,
                is_active=True,
                is_verified=True
            )
            db.add(admin)
            
            # Create sample doctor
            doctor = User(
                email="doctor@medicalcycle.local",
                username="doctor",
                full_name="Dr. John Smith",
                hashed_password=hash_password("doctor123"),
                role=UserRole.DOCTOR,
                is_active=True,
                is_verified=True,
                license_number="DOC123456"
            )
            db.add(doctor)
            
            # Create sample pharmacist
            pharmacist = User(
                email="pharmacist@medicalcycle.local",
                username="pharmacist",
                full_name="Jane Pharmacy",
                hashed_password=hash_password("pharmacist123"),
                role=UserRole.PHARMACIST,
                is_active=True,
                is_verified=True,
                license_number="PHARM123456"
            )
            db.add(pharmacist)
            
            # Create sample patient
            patient = User(
                email="patient@medicalcycle.local",
                username="patient",
                full_name="John Patient",
                hashed_password=hash_password("patient123"),
                role=UserRole.PATIENT,
                is_active=True,
                is_verified=True
            )
            db.add(patient)
            
            db.commit()
            
            print("✅ Database initialized successfully!")
            print("\nDefault credentials:")
            print("  Admin: admin@medicalcycle.local / admin123")
            print("  Doctor: doctor@medicalcycle.local / doctor123")
            print("  Pharmacist: pharmacist@medicalcycle.local / pharmacist123")
            print("  Patient: patient@medicalcycle.local / patient123")
        else:
            print("✅ Database already initialized!")
    
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        db.rollback()
    
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
