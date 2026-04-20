from sqlalchemy import select,update,delete,or_,and_,func,asc
from models.repo_models.base_repo_model import BaseRepoModel
from ..models.account_model import Accounts,String
from schemas.v1.db_schemas.account_schema import CreateAccountDbSchema,UpdateAccountDbSchema
from core.decorators.error_handler_dec import catch_errors
from hyperlocal_platform.core.decorators.db_session_handler_dec import start_db_transaction
from sqlalchemy.ext.asyncio import AsyncSession
from hyperlocal_platform.core.enums.timezone_enum import TimeZoneEnum


class AccountRepo(BaseRepoModel):

    def __init__(self, session:AsyncSession):
        super().__init__(session)
        self.account_cols=(
            Accounts.id,
            Accounts.name,
            Accounts.email,
            Accounts.accessed,
            Accounts.source,
            Accounts.mobile_number
        )

    @start_db_transaction
    async def create(self,data:CreateAccountDbSchema):
        self.session.add(Accounts(**data.model_dump(mode="json")))
        return True
    

    @start_db_transaction
    async def update(self,data:UpdateAccountDbSchema):
        acc_toupdate=(
            update(
                Accounts
            )
            .where(Accounts.id==data.id)
            .values(
                **data.model_dump(mode="json",exclude=['id'])
            )
        ).returning(Accounts.id)

        is_updated=(await self.session.execute(acc_toupdate)).scalar_one_or_none()
        return is_updated
    

    @start_db_transaction
    async def delete(self,account_id:str):
        acc_todel=(
            delete(
                Accounts
            )
            .where(Accounts.id==account_id)
        ).returning(Accounts.id)

        is_deleted=(await self.session.execute(acc_todel)).scalar_one_or_none()
        return is_deleted
    

    async def get(self,query:str,limit:int,offset:int,timezone:TimeZoneEnum):
        search_term=f"%{query}%"
        cursor=(offset-1)*limit
        created_at=func.date(func.timezone(timezone.value,Accounts.created_at))

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
            .limit(limit=limit)
            .order_by(asc(Accounts.created_at))
        )

        accounts=(await self.session.execute(account_stmt)).mappings().all()

        return accounts
    


    async def getby_id(self,account_id:str,timezone:TimeZoneEnum):
        created_at=func.date(func.timezone(timezone.value,Accounts.created_at))

        account_stmt=(
            select(
                *self.account_cols,
                created_at
            )
            .where(
                Accounts.id==account_id
            )
        )

        account=(await self.session.execute(account_stmt)).mappings().one_or_none()

        return account
    

    async def search(self,query:str,limit:int):
        search_term=f"%{query}%"

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
            .limit(limit=limit)
        )

        accounts=(await self.session.execute(account_stmt)).mappings().all()

        return accounts

    