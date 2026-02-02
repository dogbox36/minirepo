from typing import Optional

from pydantic import BaseModel


class Geo(BaseModel):
    lat: str
    lng: str


class Address(BaseModel):
    street: str
    suite: str
    city: str
    zipcode: str
    geo: Geo


class Company(BaseModel):
    name: str
    catchPhrase: str
    bs: str


class UserBase(BaseModel):
    name: str
    username: str
    email: str
    # Making these optional because POST response might not include them all
    phone: Optional[str] = None
    website: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    address: Optional[Address] = None
    company: Optional[Company] = None

    class Config:
        from_attributes = True


# JsonPlaceholder returns a direct list, not wrapped in 'data'
# So we don't need ListUsersResponse with pagination fields, just a type alias or list model check.
