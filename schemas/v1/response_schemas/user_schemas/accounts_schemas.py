from typing import Optional,List
from core.data_formats.enums.account_enums import AccountsAccessEnum
from pydantic import BaseModel,EmailStr
from datetime import datetime


class AccountsGetResponseSchema(BaseModel):
    id:str
    name:str
    mobile_number:str
    email:EmailStr
    created_at:datetime
    updated_at:datetime

class AccountsCreateResponseSchema(BaseModel):
    id:str
    name:str
    mobile_number:str
    email:EmailStr
    created_at:datetime
    

class AccountsUpdateResponseSchema(BaseModel):
    id:str
    name:str
    mobile_number:str
    email:EmailStr
    created_at:datetime
    updated_at:datetime

class AccountsDeleteResponseSchema(BaseModel):
    id:str
    name:str
    mobile_number:str
    email:EmailStr
    created_at:datetime
