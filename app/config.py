from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_username: str
    database_password: str
    database_name: str
    secret_key: str
    alogrithm: str
    access_token_expire_minutes: int
    sendgrid_api_key: str

    class Config:
        env_file = ".env"  # .env file path


settings = Settings()
