from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..core.dependencies.db_dependencies import get_db
from ..core.dependencies.perm_dependencies import permission_required
from ..models.users import schema, crud
from ..models.users.user import User, Permission, Role, AuditLog, Group
from typing import List, Optional

router = APIRouter(
    prefix="/users",
    responses={404: {"description": "Not found"}}
    )

def fake_hash_password(password: str): # later change to used advanced hashing method
    return "fakehashed" + password

# USER

@router.get("/", response_model=List[schema.UserListResponse], dependencies=[Depends(permission_required("user:read"))], tags=["user"])
def get_user_list(
    limit: int = Query(10, ge=1), 
    skip: int = Query(0, ge=0), 
    username: Optional[List[str]] = Query(None), 
    email: Optional[List[str]] = Query(None), 
    db: Session = Depends(get_db)
):
    return crud.get_user_list(db, limit, skip, username, email)

@router.post("/", response_model=schema.UserCreate, dependencies=[Depends(permission_required("user:create"))], tags=["user"])
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    hashed_password = fake_hash_password(user.password)
    db_user = User(id=user.id, username=user.username.lower(), email=user.email.lower(), password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.put("/", response_model=schema.UserUpdate, dependencies=[Depends(permission_required("user:update"))], tags=["user"])
def update_user(user_id: int, user: schema.UserUpdate, db: Session = Depends(get_db)): # TEMPORARY
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    
    # should add method to update current user details for permissions later OR ReLogin if current user update its own details
    # later create another dependencies to check current user = db_user id, then it can update.

    return db_user

@router.delete("/delete/{user_id}", dependencies=[Depends(permission_required("user:delete"))], tags=["user"])
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    return crud.delete_user(db, user_id)

# ROLE

@router.post("/roles/", 
             response_model=schema.RoleCreate, 
             dependencies=[Depends(permission_required("user:create"))],
             tags=["roles"])
def create_role(role: schema.RoleCreate, db: Session = Depends(get_db)):
    db_role = Role(id=role.id, name=role.name.lower())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

@router.get("/roles/", 
            response_model=List[schema.Role], 
            dependencies=[Depends(permission_required("user:read"))],
            tags=["roles"])
def read_roles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    roles = crud.get_role(db, limit, skip)
    return roles[skip:skip+limit]

@router.put("/roles/{role_id}", 
            response_model=schema.RoleUpdate, 
            dependencies=[Depends(permission_required("user:update"))],
            tags=["roles"])
def update_role(role_id: int, role: schema.RoleUpdate, db: Session = Depends(get_db)):
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if db_role is None:
        raise HTTPException(status_code=404, detail="role not found")
    for key, value in role.dict(exclude_unset=True).items():
        setattr(db_role, key, value)
    db.commit()
    db.refresh(db_role)
    return db_role

@router.delete("/roles/delete/{role_id}", 
               dependencies=[Depends(permission_required("user:delete"))],
               tags=["roles"])
def delete_role(
    role_id: int,
    db: Session = Depends(get_db)
):
    return crud.delete_role(db, role_id)

# Permission
@router.post("/permissions/", 
             response_model=schema.PermissionCreate, 
             dependencies=[Depends(permission_required("user:create"))],
             tags=["permissions"])
def create_permission(permission: schema.PermissionCreate, db: Session = Depends(get_db)):
    db_permission = Permission(id=permission.id, name=permission.name.lower(), details=permission.details, parentPermissionID=permission.parentPermissionID)
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission

@router.get("/permissions/", 
            response_model=List[schema.Permission], 
            dependencies=[Depends(permission_required("user:read"))],
            tags=["permissions"])
def read_permissions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    permissions = crud.get_permission_tree(db, parent_id=None)
    return permissions[skip:skip+limit]

@router.get("/permissions/{permission_id}", 
            response_model=schema.Permission, 
            dependencies=[Depends(permission_required("user:read"))],
            tags=["permissions"])
def read_permission(permission_id: int, db: Session = Depends(get_db)):
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission

@router.put("/permissions/{permission_id}", 
            response_model=schema.Permission, 
            dependencies=[Depends(permission_required("user:update"))],
            tags=["permissions"])
def update_permission(permission_id: int, permission: schema.PermissionUpdate, db: Session = Depends(get_db)):
    db_permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if db_permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    for key, value in permission.dict(exclude_unset=True).items():
        setattr(db_permission, key, value)
    db.commit()
    db.refresh(db_permission)
    return db_permission

@router.delete("/permissions/delete/{permission_id}", 
               dependencies=[Depends(permission_required("user:delete"))],
               tags=["permissions"])
def delete_permission(permission_id: int, db: Session = Depends(get_db)):
    db_permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if db_permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    temp_name = db_permission.name
    db.delete(db_permission)
    db.commit()
    return {"detail": f"{temp_name} Permission deleted"}

# Groups
@router.post("/groups/", 
             response_model=schema.GroupCreate, 
             dependencies=[Depends(permission_required("user:create"))],
             tags=["groups"])
def create_group(group: schema.GroupCreate, db: Session = Depends(get_db)):
    db_group = Group(name=group.name.lower())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

@router.delete("/groups/delete/{group_id}", 
               dependencies=[Depends(permission_required("user:delete"))],
               tags=["groups"])
def delete_group(
    group_id: int,
    db: Session = Depends(get_db)
):
    return crud.delete_group(db, group_id)


# Assingment
@router.post("/{user_id}/roles/{role_id}", 
             dependencies=[Depends(permission_required("user:create"))],
             tags=["roles"])
def assign_role_to_user(user_id: int, role_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    role = db.query(Role).filter(Role.id == role_id).first()
    if not user or not role:
        raise HTTPException(status_code=404, detail="User or Role not found")
    if role in user.roles:
        raise HTTPException(status_code=400, detail="Role already assigned to user")
    user.roles.append(role)
    db.commit()
    return {"message": "Role assigned to user"}

@router.post("/{user_id}/permissions/{permission_id}", 
             dependencies=[Depends(permission_required("user:create"))],
             tags=["permissions"])
def assign_permission_to_user(user_id: int, permission_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not user or not permission:
        raise HTTPException(status_code=404, detail="User or Permission not found")
    if permission in user.permissions:
        raise HTTPException(status_code=400, detail="Permission already assigned to user")
    user.permissions.append(permission)
    db.commit()
    return {"message": "Permission assigned to user"}

@router.post("/{user_id}/groups/{group_id}", 
             dependencies=[Depends(permission_required("user:create"))],
             tags=["groups"])
def assign_user_to_group(user_id: int, group_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    group = db.query(Group).filter(Group.id == group_id).first()
    if not user or not group:
        raise HTTPException(status_code=404, detail="User or Group not found")
    if group in user.groups:
        raise HTTPException(status_code=400, detail="User already assigned to group")
    user.groups.append(group)
    db.commit()
    return {"message": "User assigned to group"}

@router.put("/{user_id}/roles", 
            dependencies=[Depends(permission_required("user:update"))],
            tags=["roles"])
def update_user_roles(user_id: int, role_ids: List[int], db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    roles = db.query(Role).filter(Role.id.in_(role_ids)).all()
    user.roles = roles    
    db.commit()
    return {"message": "User roles updated successfully"}

@router.put("/{user_id}/permissions", 
            dependencies=[Depends(permission_required("user:update"))],
            tags=["permissions"])
def update_user_permissions(user_id: int, permission_ids: List[int], db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    permissions = db.query(Permission).filter(Permission.id.in_(permission_ids)).all()
    user.permissions = permissions
    db.commit()
    return {"message": "Role permissions updated successfully"}

@router.put("/{user_id}/groups", 
            dependencies=[Depends(permission_required("user:update"))],
            tags=["groups"])
def update_user_groups(user_id: int, group_ids: List[int], db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    groups = db.query(Group).filter(Group.id.in_(group_ids)).all()
    user.groups = groups
    db.commit()
    return {"message": "User groups updated successfully"}

@router.post("/roles/{role_id}/permissions/{permission_id}", 
             dependencies=[Depends(permission_required("user:create"))],
             tags=["permissions"])
def assign_permission_to_role(role_id: int, permission_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not role or not permission:
        raise HTTPException(status_code=404, detail="Role or Permission not found")
    if permission in role.permissions:
        raise HTTPException(status_code=400, detail="Permission already assigned to role")
    role.permissions.append(permission)
    db.commit()
    return {"message": "Permission assigned to role"}

@router.put("/roles/{role_id}/permissions", 
            dependencies=[Depends(permission_required("user:update"))],
            tags=["permissions"])
def update_role_permissions(role_id: int, permission_ids: List[int], db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    permissions = db.query(Permission).filter(Permission.id.in_(permission_ids)).all()
    role.permissions = permissions
    db.commit()
    return {"message": "Role permissions updated successfully"}

@router.post("/audit/", response_model=dict, 
             dependencies=[Depends(permission_required("user:create"))],
             tags=["auditlogs"])
def create_audit_log(user_id: int, change_type: str, change_details: dict, db: Session = Depends(get_db)):
    db_audit = AuditLog(user_id=user_id, change_type=change_type, change_details=change_details)
    db.add(db_audit)
    db.commit()
    db.refresh(db_audit)
    return {"message": "Audit log created"}
