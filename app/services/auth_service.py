from app.models.user import UserCreate, UserInDB
from app.utils.token_utils import create_access_token, verify_token
from app.config.settings import SECRET_KEY
import bcrypt
from app.database.mongodb import insert_one_into_db, get_data_from_db
from app.utils.utilities import AuthEngine
from fastapi import HTTPException, status

# Save user to database
async def create_user(user: UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    user_dict = user.dict()
    user_dict["password"] = hashed_password.decode('utf-8')

    existing_user = await get_data_from_db("users", {"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    
    user_id = await insert_one_into_db("users", user_dict)
    user_in_db = UserInDB(id=str(user_id), email=user.email, password=user_dict["password"])
    return user_in_db

# Authenticate user
async def authenticate_user(email: str, password: str):
    try:
        print(f"here connection {email}")
        user = await get_data_from_db("users", {"email": email})
        print(f"user {user}")
        if user and bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
            user["id"] = str(user["_id"])
            return UserInDB(**user)
    except Exception as e:
        print(f"Error during authentication: {e}")
        return None

# Refresh token
async def refresh_token(current_token: str, user: str):
    if await verify_token(current_token):
        new_token = await create_access_token(data={"user": user})
    AuthEngine.refreshedToken.add(current_token)
    return new_token

#Revoke token
async def revoke_token(token: str):
    print(f"token {token}")
    if token in AuthEngine.revokedToken:
            raise HTTPException(status_code=401, detail="Token already revoked")
    AuthEngine.revokedToken.add(token)
    return True

