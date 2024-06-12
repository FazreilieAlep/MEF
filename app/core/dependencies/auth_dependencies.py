from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing_extensions import Annotated
from ..dependencies.db_dependencies import get_db
from ...models.users import schema, crud

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def fake_decode_token(token):
    # This function should decode the token to get the username
    # For simplicity, we assume the token is the username
    username = token
    return username

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    username = fake_decode_token(token)
    user = crud.get_user_permission(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(
    current_user: Annotated[schema.CurrentUser, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return {"username": current_user.username, "disabled": current_user.disabled}


async def get_current_user_permission(
    current_user: Annotated[schema.UserPermissionCheck, Depends(get_current_user)],
):
    return current_user