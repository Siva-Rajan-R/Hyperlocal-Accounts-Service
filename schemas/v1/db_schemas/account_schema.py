from pydantic import BaseModel,EmailStr
from typing import List
from core.data_formats.enums.account_enums import AccountsAccessEnum


class CreateAccountDbSchema(BaseModel):
    id:str
    email:EmailStr
    mobile_number:str
    name:str
    source:str
    accessed:List[AccountsAccessEnum]


class UpdateAccountDbSchema(BaseModel):
    id:str
    mobile_number:str
    name:str