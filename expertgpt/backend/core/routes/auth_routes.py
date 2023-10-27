import os
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
import secrets
from pg.users import is_user_in_db, add_user_in_db


# define user password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Token settings
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

auth_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Add your database model
class UserInDB:
    def __init__(self, hashed_password):
        self.hashed_password = hashed_password

# Sign 
@auth_router.post(
    "/signup",
    tags=["Authentication"],
)
async def sign_up(
    email: str,
    password: str,
):
    hashed_password = get_password_hash(password)
    
    if is_user_in_db(email=email):
        return {"message": "You are already signed up", "type": "Error"}

    user_id = add_user_in_db(email=email)
    # add your logic to save the user to your database
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": hashed_password, "user_id": str(user_id), "email": email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

    