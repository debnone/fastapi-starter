from logging import log
from fastapi.exceptions import HTTPException
from fastapi import status, APIRouter
from fastapi.params import Depends
from passlib.context import CryptContext
from .config import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import random
import string
from .database import engine, get_db
from sqlalchemy.orm import Session
from . import models, schemas, utils, oauth2


router = APIRouter(prefix="/users", tags=["users"])


SENDGRID_API_KEY = settings.sendgrid_api_key

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hash_password):
    return pwd_context.verify(plain_password, hash_password)


def generate_reset_code():
    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(6)
    )


# Sendgrid email function
def send_email(email, subject, message):
    message = Mail(
        from_email="tamerdabsan@gmail.com",
        to_emails=email,
        subject=subject,
        html_content=message,
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)


# TODO: twilio send sms function

# def send_sms(phone_number, message):
#     from twilio.rest import Client

#     account_sid = settings.twilio_account_sid
#     auth_token = settings.twilio_auth_token
#     client = Client(account_sid, auth_token)
#     message = client.messages.create(
#         body=message, from_=settings.twilio_phone_number, to=phone_number,
#     )
#     return message.sid


# status code function
def code(status_code):
    if status_code == 400:
        return status.HTTP_400_BAD_REQUEST
    elif status_code == 401:
        return status.HTTP_401_UNAUTHORIZED
    elif status_code == 403:
        return status.HTTP_403_FORBIDDEN
    elif status_code == 404:
        return status.HTTP_404_NOT_FOUND


# HTTPException response function
def Error(code, message):
    return HTTPException(status_code=code, detail=message)


def schema_type(schemas):
    if schemas == "user":
        return schemas.UserUpdate
    elif schemas == "phoneNumber":
        return schemas.PhoneNumberUpdate
    elif schemas == "city":
        return schemas.CityUpdate

    phone_number: str
    first_name: str
    last_name: str
    city: str
    street: str
    house_number: str


def update_logic(schema_type, id, updated_info, db, current_user):
    if current_user != id:
        raise Error(code(403), "You are not authorized to update this user")
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise Error(code(404), "User not found")
    if schema_type == "user":
        if updated_info.email:
            user.email = updated_info.email
        if updated_info.first_name:
            user.first_name = updated_info.first_name
        if updated_info.last_name:
            user.last_name = updated_info.last_name
        if updated_info.password:
            user.password = hash(updated_info.password)
    elif schema_type == "phoneNumber":
        if updated_info.phone_number:
            user.phone_number = updated_info.phone_number
    elif schema_type == "city":
        if updated_info.city:
            user.city = updated_info.city
    elif schema_type == "street":
        if updated_info.street:
            user.street = updated_info.street
    elif schema_type == "houseNumber":
        if updated_info.house_number:
            user.house_number = updated_info.house_number
    db.commit()
    return user


def update_user(
    id: int,
    updated_info: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    if current_user != id:
        raise Error(code(403), "You are not authorized to update this user")
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise Error(code(404), "User not found")
    if updated_info.email:
        user.email = updated_info.email
    if updated_info.first_name:
        user.first_name = updated_info.first_name
    if updated_info.last_name:
        user.last_name = updated_info.last_name
    if updated_info.password:
        user.password = hash(updated_info.password)
    db.commit()
    return user


# pdf receipt function


# send code html template function
def send_code_html(code, language):
    if language == "en":
        header = "Welcome"
        paragraph = "your code is"

    elif language == "ar":
        header = "مرحبا"
        paragraph = "الكود هو"
    elif language == "heb":
        header = "ברוכים הבאים"
        paragraph = "הקוד שלך הוא"

    return f"""
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HTML Email</title>
    <style type="text/css">
    </style>
  </head>
  <body style="margin:0;padding:0;background-color:#f6f9fc;">
    <center class="wrapper" style="width:100%;table-layout:fixed;background-color:#f6f9fc;padding-bottom:40px;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;">
      <div class="webkit" style="max-width:600px;background-color:#ffffff;margin:0 auto;">
        <table class="output" align="center" style="border-spacing:0;">
          <tr>
            <td style="padding:0;">
              <table width="100%" style="border-spacing:0;border-spacing: 0px; border-collapse:0;">
                <tr>
                  <td style="padding:0;">
                    <h1>{header}</h1>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          <tr>
            <td style="padding:0;">
              <h2>{paragraph}</h2>
            </td>
          </tr>
          <tr>
            <td >
              <h1 style="text-align: center; border: 1px solid; border-radius: 7px; margin: 0 auto; padding: 5px 5px 5px;">{code}</h1>
            </td>
          </tr>
        </table>
      </div>
    </center>
  </body>
</html>
    """

