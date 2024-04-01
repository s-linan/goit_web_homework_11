from fastapi import APIRouter, HTTPException, Depends, status, Path, Query, Security
from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from src.database.db import get_db
from src.repository import users as repositories_users
from src.schemas.user import UserSchema, TokenSchema, UserResponse
from src.services.auth import auth_service
router = APIRouter(prefix='/auth', tags=['auth'])


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserSchema, db: AsyncSession = Depends(get_db)):
    exist_user = await repositories_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repositories_users.create_user(body, db)
    return new_user


@router.post("/login")
async def login(body: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    pass
    # user = db.query(User).filter(User.email == body.username).first()
    # if user is None:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    # if not hash_handler.verify_password(body.password, user.password):
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    # # Generate JWT
    # access_token = await create_access_token(data={"sub": user.email})
    # refresh_token = await create_refresh_token(data={"sub": user.email})
    # user.refresh_token = refresh_token
    # db.commit()
    # return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/refresh_token')
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(), db: AsyncSession = Depends(get_db)):
    pass
    token = credentials.credentials
    # email = await get_email_form_refresh_token(token)
    # user = db.query(User).filter(User.email == email).first()
    # if user.refresh_token != token:
    #     user.refresh_token = None
    #     db.commit()
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    #
    # access_token = await create_access_token(data={"sub": email})
    # refresh_token = await create_refresh_token(data={"sub": email})
    # user.refresh_token = refresh_token
    # db.commit()
    # return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
