from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey, JSON, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from sqlalchemy.sql.functions import current_timestamp
from ...core.database import Base
from .associations import user_roles, user_permissions,user_groups, role_permissions

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    disabled = Column(Boolean, nullable=True, default=False)
    roles = relationship('Role', secondary=user_roles, back_populates='users')
    permissions = relationship('Permission', secondary=user_permissions, back_populates='users')
    groups = relationship('Group', secondary=user_groups, back_populates='users')

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    users = relationship('User', secondary=user_roles, back_populates='roles')
    permissions = relationship('Permission', secondary=role_permissions, back_populates='roles')

class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    details = Column(JSON, nullable=False)
    parentPermissionID = Column(Integer, ForeignKey('permissions.id'), nullable=True)
    roles = relationship('Role', secondary=role_permissions, back_populates='permissions')
    users = relationship('User', secondary=user_permissions, back_populates='permissions')
    parent_permission = relationship('Permission', remote_side=[id], backref='child_permissions')

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    users = relationship('User', secondary=user_groups, back_populates='groups')

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    change_type = Column(String(50))
    change_details = Column(JSON)
    changed_at = Column(TIMESTAMP, server_default=func.now())
    user = relationship('User')