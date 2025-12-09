"""Audit logging utilities"""
from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog, AuditAction
from uuid import UUID
from typing import Optional
from datetime import datetime


def log_audit(
    db: Session,
    user_id: Optional[UUID],
    action: AuditAction,
    resource_type: str,
    resource_id: Optional[UUID] = None,
    description: Optional[str] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    status: str = "success",
    error_message: Optional[str] = None
) -> AuditLog:
    """Log an audit event"""
    audit_log = AuditLog(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        description=description,
        ip_address=ip_address,
        user_agent=user_agent,
        status=status,
        error_message=error_message,
        timestamp=datetime.utcnow()
    )
    db.add(audit_log)
    db.commit()
    db.refresh(audit_log)
    return audit_log


def get_audit_logs(
    db: Session,
    user_id: Optional[UUID] = None,
    resource_type: Optional[str] = None,
    resource_id: Optional[UUID] = None,
    limit: int = 100,
    offset: int = 0
) -> list:
    """Get audit logs with optional filters"""
    query = db.query(AuditLog)
    
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)
    
    if resource_type:
        query = query.filter(AuditLog.resource_type == resource_type)
    
    if resource_id:
        query = query.filter(AuditLog.resource_id == resource_id)
    
    return query.order_by(AuditLog.timestamp.desc()).offset(offset).limit(limit).all()
