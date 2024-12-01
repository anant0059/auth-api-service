from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import UserCreate
from app.services.auth_service import create_user, authenticate_user, refresh_token, revoke_token
from fastapi.security import OAuth2PasswordBearer
from app.utils.token_utils import create_access_token, verify_token, get_token_from_header

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 1. Sign up
@router.post("/signup")
async def sign_up(user: UserCreate):
    db_user = await create_user(user)
    token = await create_access_token(data={"user": db_user.email})
    return {"message": "User created successfully","access_token": token, "token_type": "bearer"}

# 2. Sign in
@router.post("/signin")
async def sign_in(user: UserCreate):
    db_user = await authenticate_user(user.email, user.password)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = await create_access_token(data={"user": db_user.email})
    return {"access_token": token, "token_type": "bearer"}

# 3. Authorization of token
@router.get("/protected-endpoint")
async def protected_endpoint(token: str = Depends(get_token_from_header)):
    user_data = await verify_token(token)
    return {"message": "Access granted", "user": user_data}

# 4. Revocation of token
@router.post("/revoke-token")
async def revoke(token: str = Depends(get_token_from_header)):
    user_data = await verify_token(token)
    result = await revoke_token(token)
    if not result:
        raise HTTPException(status_code=400, detail="Token revocation failed")
    return {"message": "Token revoked successfully"}

# 5. Refresh of token
@router.post("/refresh-token")
async def refresh_access_token(token: str = Depends(oauth2_scheme)):
    user_data = await verify_token(token)
    user = user_data.get("user")
    
    new_token = await refresh_token(token, user)
    if new_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    
    return {"access_token": new_token, "token_type": "bearer"}
