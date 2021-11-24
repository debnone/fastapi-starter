from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app import schemas
from app.main import app
from app.config import settings
from app.database import get_db
from app.database import Base


# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Tgm634476@localhost:5432/fastapi_test"
# Down here we are using the same database as the one we are testing. but we are using a different name of database.
# we add the database name at the end of the url in a f string.
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False,
)


@pytest.fixture()
def session():
    # run our code after we run the test
    Base.metadata.drop_all(bind=engine)  # drop the database before/after the test
    # run our code before we run the test
    Base.metadata.create_all(bind=engine)  # create the database if it doesn't exist

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
