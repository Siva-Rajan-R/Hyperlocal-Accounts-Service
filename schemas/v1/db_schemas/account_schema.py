from pydantic import BaseModel,EmailStr
from typing import List


class CreateAccountDbSchema(BaseModel):
    id:str
    email:EmailStr
    mobile_number:str
    name:str
    source:str
    accessed:List[str]


class UpdateAccountDbSchema(BaseModel):
    id:str
    mobile_number:str
    name:str