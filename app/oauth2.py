from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import schemas, database, models
from .config import settings


oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.alogrithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def _get_access_token_expiration_time():
    return datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)


def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": _get_access_token_expiration_time()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_expiration):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_expiration
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_expiration
    return token_data


def get_current_user(
    token: str = Depends(oauth2_schema), db: Session = Depends(database.get_db)
):
    credentials_expiration = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token, credentials_expiration)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user


# access token refresher function for fastapi   #expirement
def token_refresher(token: str = Depends(oauth2_schema)):
    credentials_expiration = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token, credentials_expiration)
    return create_access_token({"user_id": token.id})

