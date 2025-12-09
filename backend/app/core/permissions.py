"""Permission and authorization utilities"""
from enum import Enum
from app.models.user import UserRole


class Permission(str, Enum):
    """Permissions"""
    # User permissions
    CREATE_USER = "create_user"
    READ_USER = "read_user"
    UPDATE_USER = "update_user"
    DELETE_USER = "delete_user"
    
    # Patient permissions
    CREATE_PATIENT = "create_patient"
    READ_PATIENT = "read_patient"
    UPDATE_PATIENT = "update_patient"
    DELETE_PATIENT = "delete_patient"
    
    # Consultation permissions
    CREATE_CONSULTATION = "create_consultation"
    READ_CONSULTATION = "read_consultation"
    UPDATE_CONSULTATION = "update_consultation"
    DELETE_CONSULTATION = "delete_consultation"
    
    # Prescription permissions
    CREATE_PRESCRIPTION = "create_prescription"
    READ_PRESCRIPTION = "read_prescription"
    UPDATE_PRESCRIPTION = "update_prescription"
    DELETE_PRESCRIPTION = "delete_prescription"
    DISPENSE_PRESCRIPTION = "dispense_prescription"
    
    # Audit permissions
    READ_AUDIT_LOG = "read_audit_log"


# Role-based permissions mapping
ROLE_PERMISSIONS = {
    UserRole.ADMIN: [
        Permission.CREATE_USER,
        Permission.READ_USER,
        Permission.UPDATE_USER,
        Permission.DELETE_USER,
        Permission.CREATE_PATIENT,
        Permission.READ_PATIENT,
        Permission.UPDATE_PATIENT,
        Permission.DELETE_PATIENT,
        Permission.CREATE_CONSULTATION,
        Permission.READ_CONSULTATION,
        Permission.UPDATE_CONSULTATION,
        Permission.DELETE_CONSULTATION,
        Permission.CREATE_PRESCRIPTION,
        Permission.READ_PRESCRIPTION,
        Permission.UPDATE_PRESCRIPTION,
        Permission.DELETE_PRESCRIPTION,
        Permission.DISPENSE_PRESCRIPTION,
        Permission.READ_AUDIT_LOG,
    ],
    UserRole.DOCTOR: [
        Permission.READ_USER,
        Permission.READ_PATIENT,
        Permission.UPDATE_PATIENT,
        Permission.CREATE_CONSULTATION,
        Permission.READ_CONSULTATION,
        Permission.UPDATE_CONSULTATION,
        Permission.CREATE_PRESCRIPTION,
        Permission.READ_PRESCRIPTION,
        Permission.UPDATE_PRESCRIPTION,
    ],
    UserRole.NURSE: [
        Permission.READ_PATIENT,
        Permission.UPDATE_PATIENT,
        Permission.READ_CONSULTATION,
        Permission.UPDATE_CONSULTATION,
        Permission.READ_PRESCRIPTION,
    ],
    UserRole.PHARMACIST: [
        Permission.READ_PATIENT,
        Permission.READ_PRESCRIPTION,
        Permission.UPDATE_PRESCRIPTION,
        Permission.DISPENSE_PRESCRIPTION,
    ],
    UserRole.PATIENT: [
        Permission.READ_USER,
        Permission.UPDATE_USER,
        Permission.READ_PATIENT,
        Permission.UPDATE_PATIENT,
        Permission.READ_CONSULTATION,
        Permission.READ_PRESCRIPTION,
    ],
}


def has_permission(role: UserRole, permission: Permission) -> bool:
    """Check if a role has a specific permission"""
    return permission in ROLE_PERMISSIONS.get(role, [])


def get_role_permissions(role: UserRole) -> list:
    """Get all permissions for a role"""
    return ROLE_PERMISSIONS.get(role, [])
