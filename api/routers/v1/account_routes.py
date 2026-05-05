from fastapi import APIRouter,Depends,Query
from icecream import ic
from hyperlocal_platform.core.models.req_res_models import SuccessResponseTypDict,ErrorResponseTypDict,BaseResponseTypDict
from infras.primary_db.services.accounts_service import AccountService,Optional,TimeZoneEnum
from schemas.v1.request_schemas.account_schema import CreateAccountSchema,UpdateAccountSchema,DeleteAccountSchema,GetAccountByIdSchema,GetAccountsSchema
from schemas.v1.response_schemas.user_schemas.accounts_schemas import AccountsGetResponseSchema,AccountsCreateResponseSchema,AccountsDeleteResponseSchema,AccountsUpdateResponseSchema
from infras.primary_db.main import get_pg_async_session,AsyncSession
from typing import Annotated,List


router=APIRouter(
    tags=['Accounts CRUD'],
    prefix='/accounts'
)

PG_ASYNC_SESSION=Annotated[AsyncSession,Depends(get_pg_async_session)]


# Write methods
@router.post('/')
async def create(data:CreateAccountSchema,session:PG_ASYNC_SESSION):
    res=await AccountService(session=session).create(data=data)
    ic(res)
    return SuccessResponseTypDict(
        detail=BaseResponseTypDict(
            msg="Successfully account created",
            status_code=201,
            success=True
        ),
        data=AccountsCreateResponseSchema(**res) if res else None
    )

@router.put('/')
async def update(data:UpdateAccountSchema,session:PG_ASYNC_SESSION):
    res=await AccountService(session=session).update(data=data)
    ic(res)
    return SuccessResponseTypDict(
        detail=BaseResponseTypDict(
            msg="Account Updated Successfully",
            status_code=200,
            success=True
        ),
        data=AccountsUpdateResponseSchema(**res) if res else None
    )


@router.delete('/{account_id}')
async def delete(session:PG_ASYNC_SESSION,data: DeleteAccountSchema=Depends()):
    res=await AccountService(session=session).delete(data=data)
    ic(res)
    return SuccessResponseTypDict(
        detail=BaseResponseTypDict(
            msg="Account Deleted Successfully",
            status_code=200,
            success=True
        ),
        data=AccountsDeleteResponseSchema(**res) if res else None
    )

# Read methods
@router.get('/by/{account_id}')
async def get_accid(session:PG_ASYNC_SESSION,data:GetAccountByIdSchema=Depends()):
    res = await AccountService(session=session).getby_id(data=data)
    ic(res)

    return SuccessResponseTypDict(
        detail=BaseResponseTypDict(
            msg="Account Fetched Successfully",
            success=True,
            status_code=200
        ),
        data=AccountsGetResponseSchema(**res) if res else None
    )



@router.get('/')
async def get_all(session:PG_ASYNC_SESSION,data:GetAccountsSchema=Depends()):
    res = await AccountService(session=session).get(data=data)
    ic(res)
    return SuccessResponseTypDict(
        detail=BaseResponseTypDict(
            msg="Account fetched successfully",
            status_code=200,
            success=True
        ),
        data=[AccountsGetResponseSchema(**r) for r in res] if res else None
    )

# @router.get('/search')
# async def search(session:PG_ASYNC_SESSION,q:str,limit:Optional[int]=Query(5)):
#     return await AccountService(session=session).search(query=q,limit=limit)



