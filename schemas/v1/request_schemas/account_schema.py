from pydantic import BaseModel,EmailStr,Field
from typing import List,Optional
from core.data_formats.enums.account_enums import AccountsAccessEnum
from hyperlocal_platform.core.enums.timezone_enum import TimeZoneEnum

# WRITABLE SCHEMAS
class CreateAccountSchema(BaseModel):
    email:EmailStr
    mobile_number:str
    name:str
    source:str
    accessed:List[AccountsAccessEnum]


class UpdateAccountSchema(BaseModel):
    id:str
    mobile_number:str
    name:str

class DeleteAccountSchema(BaseModel):
    account_id:str


# FETCHABLE SCHEMAS

class VerifyAccountSchema(BaseModel):
    account_id:Optional[str]=None
    email:Optional[EmailStr]=None
    mobile_number:Optional[str]=None

class GetAccountsSchema(BaseModel):
    offset:int
    query:Optional[str]=Field(default="",alias="q")
    limit:Optional[int]=Field(default=10,le=100)
    timezone:Optional[TimeZoneEnum]=TimeZoneEnum.Asia_Kolkata

    model_config={
        "populate_by_name":True
    }

class GetAccountByIdSchema(BaseModel):
    account_id:str
    timezone:Optional[TimeZoneEnum]=TimeZoneEnum.Asia_Kolkata