from pytz import timezone
from sqlalchemy import select,update,delete,or_,and_,func,asc,insert
from models.repo_models.base_repo_model import BaseRepoModel
from ..models.account_model import Accounts,String
from schemas.v1.db_schemas.account_schema import CreateAccountDbSchema,UpdateAccountDbSchema
from schemas.v1.request_schemas.account_schema import VerifyAccountSchema,GetAccountsSchema,GetAccountByIdSchema,DeleteAccountSchema
from core.decorators.error_handler_dec import catch_errors
from hyperlocal_platform.core.decorators.db_session_handler_dec import start_db_transaction
from sqlalchemy.ext.asyncio import AsyncSession
from hyperlocal_platform.core.enums.timezone_enum import TimeZoneEnum
from typing import List
from icecream import ic


class AccountRepo(BaseRepoModel):

    def __init__(self, session:AsyncSession):
        super().__init__(session)
        self.account_cols=(
            Accounts.id,
            Accounts.sequence_id,
            Accounts.name,
            Accounts.email,
            Accounts.mobile_number,
            Accounts.source,
            Accounts.accessed,
            Accounts.created_at,
            Accounts.updated_at
        )

    @start_db_transaction
    async def create(self,data:CreateAccountDbSchema)-> dict | None:
        stmt = (
            insert(Accounts)
            .values(**data.model_dump(mode="json"))
            .returning(*self.account_cols)
        )
        ic(data.model_dump(mode="json"))
        account=(await self.session.execute(stmt)).mappings().one_or_none()
        return account
    

    @start_db_transaction
    async def update(self,data:UpdateAccountDbSchema)-> dict | None:
        acc_toupdate=(
            update(
                Accounts
            )
            .where(Accounts.id==data.id)
            .values(
                **data.model_dump(mode="json",exclude=['id'])
            )
        ).returning(self.account_cols)

        is_updated=(await self.session.execute(acc_toupdate)).mappings().one_or_none()
        
        return is_updated
    

    @start_db_transaction
    async def delete(self,data:DeleteAccountSchema)-> dict | None:
        acc_todel=(
            delete(
                Accounts
            )
            .where(Accounts.id==data.account_id)
        ).returning(self.account_cols)

        is_deleted=(await self.session.execute(acc_todel)).mappings().one_or_none()

        return is_deleted
    

    async def get(self,data:GetAccountsSchema)-> List[dict] | list:
        search_term=f"%{data.query}%"
        cursor=(data.offset-1)*data.limit
        created_at=func.date(func.timezone(data.timezone.value,Accounts.created_at))

        account_stmt=(
            select(
                *self.account_cols,
                created_at
            )
            .where(
                and_(
                    or_(
                        Accounts.id.ilike(search_term),
                        Accounts.name.ilike(search_term),
                        Accounts.email.ilike(search_term),
                        Accounts.mobile_number.ilike(search_term),
                        Accounts.source.ilike(search_term),
                        Accounts.accessed.any(search_term),
                        func.cast(created_at,String).ilike(search_term)
                    ),
                    Accounts.sequence_id>cursor
                )
            )
            .limit(limit=data.limit)
            .order_by(asc(Accounts.created_at))
        )

        accounts=(await self.session.execute(account_stmt)).mappings().all()

        return accounts
    


    async def getby_id(self,data:GetAccountByIdSchema)-> str|None:
        created_at=func.date(func.timezone(data.timezone.value,Accounts.created_at))

        account_stmt=(
            select(
                *self.account_cols,
                created_at
            )
            .where(
                Accounts.id==data.account_id
            )
        )

        account=(await self.session.execute(account_stmt)).mappings().one_or_none()

        return account
    
    async def verify_account(self,data:VerifyAccountSchema)-> dict:
        account_stmt=(
            select(
                Accounts.id
            )
            .where(
                or_(
                    Accounts.id==data.account_id,
                    Accounts.email==data.email,
                    Accounts.mobile_number==data.mobile_number
                )
            )
        )

        account=(await self.session.execute(account_stmt)).scalar_one_or_none()
        if account:
            return {'id':account,'exists':True}
        return {'id':'','exists':False}

    async def search(self,data:GetAccountsSchema)-> dict | None:
        search_term=f"%{data.query}%"

        account_stmt=(
            select(
                Accounts.id,
                Accounts.name,
                Accounts.email,
                Accounts.mobile_number
            )
            .where(
                or_(
                    Accounts.id.ilike(search_term),
                    Accounts.name.ilike(search_term),
                    Accounts.email.ilike(search_term),
                    Accounts.mobile_number.ilike(search_term),
                    Accounts.source.ilike(search_term),
                    Accounts.accessed.any(search_term),
                )
            )
            .limit(limit=data.limit)
        )

        accounts=(await self.session.execute(account_stmt)).mappings().all()

        return accounts

    