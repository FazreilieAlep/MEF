from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Callable
from ...models.users.schema import UserPermissionCheck
from ..dependencies.db_dependencies import get_db
from ..dependencies.auth_dependencies import get_current_user_permission

def permission_required(permission_name: str) -> Callable:
    async def permission_dependency(
        current_user: UserPermissionCheck = Depends(get_current_user_permission), 
        db: Session = Depends(get_db)
    ):
        # Check user permissions
        user_permissions = {perm.name for perm in (current_user.permissions or [])}
        
        # Check role permissions
        role_permissions = {perm.name for role in (current_user.roles or []) for perm in (role.permissions or [])}
        
        # Combine both sets of permissions
        all_permissions = user_permissions | role_permissions
        
        if permission_name not in all_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission Denied: User does not have enough permissions to access this API"
            )
        
    return permission_dependency
