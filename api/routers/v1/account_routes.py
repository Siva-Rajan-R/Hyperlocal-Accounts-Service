from fastapi import APIRouter,Depends,Query
from infras.primary_db.services.accounts_service import AccountService,Optional,TimeZoneEnum
from schemas.v1.request_schemas.account_schema import CreateAccountSchema,UpdateAccountSchema
from infras.primary_db.main import get_pg_async_session,AsyncSession
from typing import Annotated


router=APIRouter(
    tags=['Accounts CRUD'],
    prefix='/accounts'
)

PG_ASYNC_SESSION=Annotated[AsyncSession,Depends(get_pg_async_session)]


# Write methods
@router.post('/')
async def create(data:CreateAccountSchema,session:PG_ASYNC_SESSION):
    return await AccountService(session=session).create(data=data,source="")

@router.put('/')
async def update(data:UpdateAccountSchema,session:PG_ASYNC_SESSION):
    return await AccountService(session=session).update(data=data)

@router.delete('/{account_id}')
async def delete(account_id:str,session:PG_ASYNC_SESSION):
    return await AccountService(session=session).delete(account_id=account_id)

# Read methods
@router.get('/by/{account_id}')
async def get_accid(account_id:str,session:PG_ASYNC_SESSION,timezone:Optional[TimeZoneEnum]=TimeZoneEnum.Asia_Kolkata):
    return await AccountService(session=session).getby_id(account_id=account_id,timezone=timezone)

@router.get('/search')
async def search(session:PG_ASYNC_SESSION,q:str,limit:Optional[int]=Query(5)):
    return await AccountService(session=session).search(query=q,limit=limit)

@router.get('/')
async def get_all(session:PG_ASYNC_SESSION,q:Optional[str]=Query(""),limit:Optional[int]=10,offset:int=Query(1),timezone:Optional[TimeZoneEnum]=Query(TimeZoneEnum.Asia_Kolkata)):
    return await AccountService(session=session).get(
        query=q,
        limit=limit,
        offset=offset,
        timezone=timezone
    )




