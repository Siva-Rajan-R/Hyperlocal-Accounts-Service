from sqlalchemy import select,update,delete,or_,and_,func,asc
from models.service_models.base_service_model import BaseServiceModel
from infras.primary_db.repos.accounts_repo import AccountRepo
from ..models.account_model import Accounts,String
from schemas.v1.db_schemas.account_schema import CreateAccountDbSchema,UpdateAccountDbSchema
from schemas.v1.request_schemas.account_schema import CreateAccountSchema,UpdateAccountSchema
from core.decorators.error_handler_dec import catch_errors
from hyperlocal_platform.core.decorators.db_session_handler_dec import start_db_transaction
from sqlalchemy.ext.asyncio import AsyncSession
from hyperlocal_platform.core.enums.timezone_enum import TimeZoneEnum
from typing import Optional
from fastapi.exceptions import HTTPException
from hyperlocal_platform.core.models.req_res_models import ErrorResponseTypDict,BaseResponseTypDict,SuccessResponseTypDict
from hyperlocal_platform.core.utils.uuid_generator import generate_uuid


class AccountService(BaseServiceModel):

    def __init__(self, session:AsyncSession):
        super().__init__(session)
        self.account_repo_obj=AccountRepo(session=session)

    @catch_errors
    async def create(self,data:CreateAccountSchema,source:str):
        account_id:str=generate_uuid()
        res=await self.account_repo_obj.create(data=CreateAccountDbSchema(**data.model_dump(),source=source,id=account_id,accessed=[]))
        return res
    
    @catch_errors
    async def get_or_create(self,data:CreateAccountSchema,source:str)->dict:
        account_info=await self.account_repo_obj.get(query=data.email,limit=1,offset=1,timezone=TimeZoneEnum.Asia_Kolkata)
        
        if len(account_info)<=0:
            account_id:str=generate_uuid()
            res=await self.account_repo_obj.create(data=CreateAccountDbSchema(**data.model_dump(),source=source,id=account_id,accessed=[source]))
            if res:
                data={
                    'id':account_id,
                    'email':data.email,
                    'mobile_number':data.mobile_number,
                    'name':data.name,
                    'is_new':True
                }
        else:
            fetched_data=account_info[0]
            data={
                'id':fetched_data['id'],
                'email':fetched_data['email'],
                'mobile_number':fetched_data['mobile_number'],
                'name':fetched_data['name'],
                'is_new':False
            }

        return data
    

    @catch_errors
    async def update(self,data:UpdateAccountSchema):
        res=await self.account_repo_obj.update(data=UpdateAccountDbSchema(**data.model_dump()))
        return res
    

    @catch_errors
    async def delete(self,account_id:str):
        res=await self.account_repo_obj.delete(account_id=account_id)
        return res

    

    @catch_errors
    async def get(self,offset:int,query:Optional[str]="",limit:Optional[int]=10,timezone:Optional[TimeZoneEnum]=TimeZoneEnum.Asia_Kolkata):
        res=await self.account_repo_obj.get(query=query,limit=limit,offset=offset,timezone=timezone)
        return res
    


    @catch_errors
    async def getby_id(self,account_id:str,timezone:TimeZoneEnum):
        res=await self.account_repo_obj.getby_id(account_id=account_id,timezone=timezone)
        return res
    

    @catch_errors
    async def search(self,query:str,limit:int):
        res=await self.account_repo_obj.search(query=query,limit=limit)
        return res