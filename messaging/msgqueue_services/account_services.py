from infras.primary_db.services.accounts_service import AccountService
from sqlalchemy.ext.asyncio import AsyncSession
from infras.primary_db.main import AsyncAccountDbLocalSession
from schemas.v1.request_schemas.account_schema import CreateAccountSchema,UpdateAccountSchema,VerifyAccountSchema,GetAccountByIdSchema,GetAccountsSchema,DeleteAccountSchema
from hyperlocal_platform.core.enums.timezone_enum import TimeZoneEnum
from schemas.v1.response_schemas.msgqueue_schemas.account_schemas import AccountsCreateResponseSchema,AccountsUpdateResponseSchema,AccountsDeleteResponseSchema,AccountsGetResponseSchema
from typing import Optional,List,Union
from icecream import ic

class MessagingQueueAccountService:

    async def create_account(self,data:Union[CreateAccountSchema,dict]):

        if isinstance(data, dict):
            data = CreateAccountSchema(**data)
        async with AsyncAccountDbLocalSession() as session:
            account_service_obj=AccountService(session=session)
            res=await account_service_obj.create(data=data)
            ic(res)
            if not res:
                return res
            return AccountsCreateResponseSchema(
                **res
            ).model_dump(mode="json")

    async def update_account(self,data:Union[UpdateAccountSchema,dict]):
        async with AsyncAccountDbLocalSession() as session:
            account_service_obj=AccountService(session=session)
            if isinstance(data, dict):
                data = UpdateAccountSchema(**data)
            res=await account_service_obj.update(data=data)
            if not res:
                return res
            return AccountsUpdateResponseSchema(**res).model_dump(mode="json")

    async def delete_account(self,data:Union[DeleteAccountSchema,dict]):
        async with AsyncAccountDbLocalSession() as session:
            account_service_obj=AccountService(session=session)
            if isinstance(data, dict):
                data = DeleteAccountSchema(**data)
            res=await account_service_obj.delete(data=data)
            if not res:
                return res
            return AccountsDeleteResponseSchema(**res).model_dump(mode="json")

    async def get_accounts(self,data:Union[GetAccountsSchema,dict]):
        async with AsyncAccountDbLocalSession() as session:
            account_service_obj=AccountService(session=session)
            if isinstance(data, dict):
                data = GetAccountsSchema(**data)
            res=await account_service_obj.get(data=data)
            if not res:
                return res
            return [AccountsGetResponseSchema(**r).model_dump(mode="json") for r in res]
    
    async def get_account_by_id(self,data:Union[GetAccountByIdSchema,dict]):
        async with AsyncAccountDbLocalSession() as session:
            account_service_obj=AccountService(session=session)
            if isinstance(data, dict):
                data = GetAccountByIdSchema(**data)
            res=await account_service_obj.getby_id(data=data)
            if not res:
                return res 
            return AccountsGetResponseSchema(**res).model_dump(mode="json")
        
    async def verify_account(self,data:Union[VerifyAccountSchema,dict])-> bool:
        ic(data)
        async with AsyncAccountDbLocalSession() as session:
            account_service_obj=AccountService(session=session)
            if isinstance(data, dict):
                data = VerifyAccountSchema(**data)
            res=await account_service_obj.verify_account(data=data)
            return res