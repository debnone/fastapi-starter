from ..database import engine, get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, status, Response, APIRouter
from fastapi.params import Body, Depends
from .. import models, schemas, utils, oauth2


Error = utils.Error


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    code = utils.generate_reset_code()
    email_code = utils.send_code_html(code, language="heb")
    user.validate_email_code = code
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    utils.send_email(
        user.email, "Virfy yor email", email_code,
    )

    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    print(user)
    if not user:
        raise Error(
            404, f"User with id {id} does not exist",
        )
    return user


# update user info
@router.put("/update-user/{id}", response_model=schemas.NewUpdateUser)
async def update_user(
    id: int,
    updated_info: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()
    print(user)
    if not user:
        raise Error(
            404, f"user with id {id} does not exist",
        )
    if user.id != current_user.id:
        raise Error(
            403, f"user with id {id} is not owned by current user",
        )
    user_query.update(updated_info.dict(), synchronize_session=False)
    db.commit()
    return user_query.first()
