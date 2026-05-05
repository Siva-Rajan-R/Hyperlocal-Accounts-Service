from sqlalchemy import select,update,delete,or_,and_,func,asc
from models.service_models.base_service_model import BaseServiceModel
from infras.primary_db.repos.accounts_repo import AccountRepo
from ..models.account_model import Accounts,String
from schemas.v1.db_schemas.account_schema import CreateAccountDbSchema,UpdateAccountDbSchema
from schemas.v1.request_schemas.account_schema import CreateAccountSchema,UpdateAccountSchema,VerifyAccountSchema,GetAccountByIdSchema,GetAccountsSchema,DeleteAccountSchema
from core.decorators.error_handler_dec import catch_errors
from hyperlocal_platform.core.decorators.db_session_handler_dec import start_db_transaction
from sqlalchemy.ext.asyncio import AsyncSession
from hyperlocal_platform.core.enums.timezone_enum import TimeZoneEnum
from typing import Optional,Union,List
from fastapi.exceptions import HTTPException
from hyperlocal_platform.core.models.req_res_models import ErrorResponseTypDict,BaseResponseTypDict,SuccessResponseTypDict
from hyperlocal_platform.core.utils.uuid_generator import generate_uuid
from pydantic import EmailStr


class AccountService(BaseServiceModel):

    def __init__(self, session:AsyncSession):
        super().__init__(session)
        self.account_repo_obj=AccountRepo(session=session)

    async def create(self,data:CreateAccountSchema)-> dict | None:
        account_id:str=generate_uuid()
        res=await self.account_repo_obj.create(data=CreateAccountDbSchema(**data.model_dump(),id=account_id))
        return res
    

    @catch_errors
    async def update(self,data:UpdateAccountSchema)-> dict | None:
        res=await self.account_repo_obj.update(data=UpdateAccountDbSchema(**data.model_dump()))
        return res
    

    @catch_errors
    async def delete(self,data:DeleteAccountSchema)-> dict | None:
        res=await self.account_repo_obj.delete(data=data)
        return res

    
    @catch_errors
    async def get(self,data:GetAccountsSchema)-> List[dict] | list:
        res=await self.account_repo_obj.get(data=data)
        return res
    

    @catch_errors
    async def getby_id(self,data:GetAccountByIdSchema)-> dict | None:
        res=await self.account_repo_obj.getby_id(data=data)
        return res
    
    @catch_errors
    async def verify_account(self,data:VerifyAccountSchema)-> dict:
        if (not data.account_id or data.account_id=="") and (not data.email or data.email=="") and (not data.mobile_number or data.mobile_number==""):
            return ErrorResponseTypDict(
                msg="At least one identifier(account_id/email/mobile_number) is required for verification",
                code="INVALID_REQUEST",
                success=False,
                status_code=422
            )
        
        res=await self.account_repo_obj.verify_account(data=data)
        return res


    @catch_errors
    async def search(self,data:GetAccountsSchema)-> dict | None:
        res=await self.account_repo_obj.search(data=data)
        return res
    

    # @catch_errors
    # async def get_or_create(self,data:CreateAccountSchema,source:str)->dict:
    #     account_info=await self.account_repo_obj.get(query=data.email,limit=1,offset=1,timezone=TimeZoneEnum.Asia_Kolkata)
        
    #     if len(account_info)<=0:
    #         account_id:str=generate_uuid()
    #         res=await self.account_repo_obj.create(data=CreateAccountDbSchema(**data.model_dump(),source=source,id=account_id,accessed=[source]))
    #         if res:
    #             data={
    #                 'id':account_id,
    #                 'email':data.email,
    #                 'mobile_number':data.mobile_number,
    #                 'name':data.name,
    #                 'is_new':True
    #             }
    #     else:
    #         fetched_data=account_info[0]
    #         data={
    #             'id':fetched_data['id'],
    #             'email':fetched_data['email'],
    #             'mobile_number':fetched_data['mobile_number'],
    #             'name':fetched_data['name'],
    #             'is_new':False
    #         }

    #     return data