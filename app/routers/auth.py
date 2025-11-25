from fastapi import HTTPException, status, Response, Depends, APIRouter
from .. import database, models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from .. database import get_db
from typing import List
from fastapi import HTTPException
from datetime import timedelta

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login')
def login(user_credentials : schemas.UserLogin, db:Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email==user_credentials.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid credential"
        )
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid credential"
        )
    
    access_token = oauth2.create_access_token(
        data={"user_id":user.id},
        expires_delta=timedelta(minutes=oauth2.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {'access_token': access_token, 'token_type':"bearer"}