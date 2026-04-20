from pydantic import BaseModel,EmailStr
from typing import List


class CreateAccountSchema(BaseModel):
    email:EmailStr
    mobile_number:str
    name:str


class UpdateAccountSchema(BaseModel):
    id:str
    mobile_number:str
    name:str