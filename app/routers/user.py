from fastapi import HTTPException, status, Depends, APIRouter
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi import HTTPException


router = APIRouter(
    prefix= "/users"
)


@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.UserRes)
def aiquest_user(user:schemas.UserCreate, db:Session=Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exist"
        )
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
