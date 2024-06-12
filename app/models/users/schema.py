from typing import List, Optional, Union
from pydantic import BaseModel

# PERMISSION
class PermissionBase(BaseModel):
    name: str
    details: dict

class PermissionCreate(PermissionBase):
    id: Optional[int] = None
    parentPermissionID: Optional[int] = None

class PermissionUpdate(PermissionBase):
    parentPermissionID: Optional[int] = None

class Permission(PermissionBase):
    id: int
    parentPermissionID: Optional[int]
    child_permissions: Optional[List['Permission']] = []

    class Config:
        orm_mode = True
        
class PermissionCheck(BaseModel):
    name: str
    
# ROLE
class RoleBase(BaseModel):
    id: Optional[int] = None
    name: str

class RoleCreate(RoleBase):
    pass
    
class RoleUpdate(BaseModel):
    name: str
    
class RoleCheck(BaseModel):
    name: str
    permissions: List[PermissionCheck]

class Role(RoleBase):
    id: int

    class Config:
        orm_mode = True

# GROUP
class GroupCreate(BaseModel):
    name: str
    

# USER
class UserBase(BaseModel):
    username: str
    disabled: Union[bool, None] = None # KIV
    
class UserLogin(UserBase):
    email: str
    password: str
    
class UserPermissionCheck(UserBase):
    permissions: List[PermissionCheck]
    roles: List[RoleCheck]
    
class UserCreate(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    password: str
    
class User(UserBase):
    id: Optional[int] = None
    
    class Config:
            orm_mode = True
            
class CurrentUser(UserBase):
    pass
            
class UserListResponse(BaseModel):
    id: int
    username: str
    email: Optional[str]
    disabled: Optional[bool]
    
class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[str]
    