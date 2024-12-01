from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.models.user import UserInDB
from app.config.settings import SECRET_KEY, ALGORITHM
from typing import Optional
from fastapi import HTTPException, Request
from app.utils.utilities import AuthEngine

# JWT Token expiration
ACCESS_TOKEN_EXPIRE_MINUTES = 30

async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire_time = datetime.now() + expire
    to_encode.update({"exp": expire_time})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def verify_token(token: str) -> Optional[dict]:
    try:
        if await is_token_revoked(token):
            raise HTTPException(status_code=401, detail="Token already revoked")
        
        if await is_token_refreshed(token):
            raise HTTPException(status_code=401, detail="Token already refreshed")
        
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        exp_timestamp = decoded_token.get('exp')
        
        if exp_timestamp < datetime.now().timestamp():
            raise HTTPException(status_code=401, detail="Token has expired")
        
        return decoded_token
    
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token") from e


async def is_token_revoked(token: str):
    return token in AuthEngine.revokedToken

async def is_token_refreshed(token: str):
    return token in AuthEngine.refreshedToken

async def get_token_from_header(request: Request) -> Optional[str]:
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")
    
    return auth_header[7:] 
