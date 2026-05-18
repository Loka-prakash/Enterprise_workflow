from fastapi import Depends, HTTPException

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from jose import jwt

from dotenv import load_dotenv

import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = os.getenv("ALGORITHM")

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    try:

        token = credentials.credentials

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )