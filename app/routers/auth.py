from fastapi import APIRouter, status, HTTPException, Response
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import engine, get_db


from .. import database, schemas, models, utils, oauth2

Error = utils.Error

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )
    if not user:
        raise Error(403, "Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise Error(403, "Invalid Credentials")
    if user.verify_email == False:
        raise Error(403, "Please verify your email")

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


# send user a reset code
@router.get("/forgot_password", response_model=schemas.UserEmail)
def get_user(user_credentials: schemas.ResetPassword, db: Session = Depends(get_db)):
    user_query = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.email)
        .first()
    )
    user = user_query
    if not user:
        raise Error(404, "User found 🙁")

    code = utils.generate_reset_code()  # generate reset code
    print(code)
    user.reset_password_code = code  # set reset code
    print(user.reset_password_code)
    db.add(user)  # add user to db
    db.commit()  # commit changes

    utils.send_email(
        user.email, "Reset Password", f"Your reset code is: {code}",
    )

    return user


# verify reset code
@router.get("/verify_reset_code", response_model=schemas.isVerifyCode)
def verify_reset_code(
    user_credentials: schemas.VerifyCode, db: Session = Depends(get_db)
):
    user_query = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.email)
        .first()
    )
    print(user_query)
    user = user_query
    if not user:
        raise Error(404, "User found")

    if user.reset_password_code != user_credentials.reset_code:
        raise Error(403, "Invalid reset code")

    user.verify_code = True
    db.commit()

    return user


# reset user password
@router.get("/reset_password", response_model=schemas.UserOut)
def reset_password(
    user_credentials: schemas.ResetPassword, db: Session = Depends(get_db)
):
    user_query = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.email)
        .first()
    )
    user = user_query
    if not user:
        raise Error(404, "User found")
    if user.verify_code != True:
        raise Error(403, "User not verified")

    user.password = utils.hash(user_credentials.password)
    user.reset_password_code = None
    user.verify_code = False
    db.commit()

    return user


# verify user email
@router.get("/verify_email", response_model=schemas.isVerifyEmail)
def verify_email(user_credentials: schemas.VerifyEmail, db: Session = Depends(get_db)):
    user_query = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.email)
        .first()
    )
    user = user_query
    if not user:
        raise Error(404, "User not found")
    if user.validate_email_code != user_credentials.email_code:
        raise Error(403, "Invalid code")

    user.verify_email = True
    user.validate_email_code = None
    db.commit()

    return user


# TODO:
# resend email verification code
# @router.get("/resend_email_verification", response_model=schemas.isResendEmail)
# def resend_email_verification(
#     user_credentials: schemas.ResendEmail, db: Session = Depends(get_db)
# ):
#     user_query = (
#         db.query(models.User)
#         .filter(models.User.email == user_credentials.email)
#         .first()
#     )
#     user = user_query
#     if not user:
#         raise Error(404, "User not found")

#     code = utils.generate_reset_code()
#     user.validate_email_code = code
#     db.commit()

# TODO: send verification code to user phone number

# @router.get("/send_verification_code", response_model=schemas.isSendVerificationCode)
# def send_verification_code(
#     user_credentials: schemas.SendVerificationCode, db: Session = Depends(get_db)
# ):
#     user_query = (
#         db.query(models.User)
#         .filter(models.User.email == user_credentials.email)
#         .first()
#     )
#     user = user_query
#     if not user:
#         raise Error(404, "User not found")

#     code = utils.generate_reset_code()
#     user.validate_phone_code = code
#     db.commit()

#     utils.send_sms(user.phone, f"Your verification code is: {code}")

#     return user

