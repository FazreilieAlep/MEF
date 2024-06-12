from fastapi import Query
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from .user import User, Role, Group, Permission
from http.client import HTTPException
from . import schema


def get_user_login(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if user:
        user_dict = {
            "username": user.username,
            "email": user.email,
            "password": user.password,
            "disabled": user.disabled
        }
        return schema.UserLogin(**user_dict)
    
def get_user_permission(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if user:
        user_dict = {
            "username": user.username,
            "disabled": user.disabled,
            "permissions": [{"name": perm.name} for perm in user.permissions],
            "roles": [{"name": role.name, "permissions": [{"name": perm.name} for perm in role.permissions]} for role in user.roles]
        }
        return schema.UserPermissionCheck(**user_dict)

def get_user_list(
    db: Session, 
    limit: int, 
    skip: int, 
    usernames: Optional[List[str]] = None, 
    emails: Optional[List[str]] = None
):
    query = db.query(User)

    if usernames or emails:
        usernames = [username.lower() for username in usernames]
        emails = [email.lower() for email in emails]
        
        username_conditions = [User.username.ilike(f"%{username}%") for username in usernames]
        email_conditions = [User.email.ilike(f"%{email}%") for email in emails]
        
        query = query.filter(
            or_(
                *username_conditions,
                *email_conditions,
            )
        )

    return query.offset(skip).limit(limit).all()

def get_role(db: Session, limit: int, skip: int):
    query = db.query(Role)
    return query.offset(skip).limit(limit).all()

def get_permission_tree(db: Session, parent_id: Optional[int] = None):
    permissions = db.query(Permission).filter(Permission.parentPermissionID == parent_id).all()
    permission_tree = []
    for permission in permissions:
        children = get_permission_tree(db, permission.id)
        permission_data = {
            "id": permission.id,
            "name": permission.name,
            "details": permission.details,
            "parentPermissionID": permission.parentPermissionID,
            "child_permissions": children
        }
        permission_tree.append(permission_data)
    return permission_tree

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"detail": "user not found"}
    temp_name = user.username
    db.delete(user)
    db.commit()
    return {"detail": f"{temp_name} with ID {user_id} deleted successfully"}

def delete_role(db: Session, role_id: int):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        return {"detail": "role not found"}
    temp_name = role.rolename
    db.delete(role)
    db.commit()
    return {"detail": f"{temp_name} with ID {role_id} deleted successfully"}

def delete_group(db: Session, group_id: int):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        return {"detail": "group not found"}
    temp_name = group.name
    db.delete(group)
    db.commit()
    return {"detail": f"{temp_name} with ID {group_id} deleted successfully"}