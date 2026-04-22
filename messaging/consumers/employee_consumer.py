from icecream import ic
from infras.primary_db.services.accounts_service import AccountService
from schemas.v1.request_schemas.account_schema import CreateAccountSchema
from hyperlocal_platform.core.models.messaging_models import CommonBaseConsumerModel
from core.errors.messaging_errors import FatalError,BussinessError,RetryableError
from ..main import RabbitMQMessagingConfig
from infras.primary_db.main import AsyncAccountDbLocalSession
from hyperlocal_platform.core.utils.routingkey_builder import generate_routingkey,RoutingkeyActions,RoutingkeyState,RoutingkeyVersions
from hyperlocal_platform.core.typed_dicts.messaging_typdict import SuccessMessagingTypDict,EventPublishingTypDict
from hyperlocal_platform.core.typed_dicts.saga_status_typ_dict import SagaStateErrorTypDict,SagaStateExecutionTypDict
from hyperlocal_platform.core.enums.error_enums import ErrorTypeSEnum
from hyperlocal_platform.core.enums.timezone_enum import TimeZoneEnum

class EmployeesConsumer(CommonBaseConsumerModel):
    
    async def create(self)->SuccessMessagingTypDict:
        async with AsyncAccountDbLocalSession() as session:
            event_data:dict=self.payload['data']
            employees_data:dict=event_data['employees']
            ic(f"Create : Headers=> {self.headers}, Payload => {self.payload} ")

            # validating the payload for creating accounts for employees, if any of the required field is missing then it will raise a bussiness error
            if not employees_data.get('email') or not employees_data.get('name') or not employees_data.get('mobile_number') or not employees_data.get('source'):
                raise BussinessError(
                    type=ErrorTypeSEnum.BUSSINESS_ERROR,
                    error=SagaStateErrorTypDict(
                        code=ErrorTypeSEnum.BUSSINESS_ERROR.value,
                        debug="Invalid payload for getting accounts info (email,mobile_number,name,source)",
                        user_msg="Invalid payload for accounts from employee"
                    )
                )
            
            data=CreateAccountSchema(
                email=employees_data['email'],
                name=employees_data['name'],
                mobile_number=employees_data['mobile_number']
            )


            res:dict=await AccountService(session=session).get_or_create(
                data=data,
                source=employees_data['source']
            )

            owner=await AccountService(session=session).getby_id(account_id=employees_data['account_id'],timezone=TimeZoneEnum.Asia_Kolkata)
            ic(owner,employees_data['account_id'])
            owner_name="Hyperlocal-Marketplace-User"
            if owner and len(owner)>0:
                owner_name=owner['name']
            res['owner_name']=owner_name
            r_key=generate_routingkey(domain="accounts",work_for="employees",action=RoutingkeyActions.CREATE,state=RoutingkeyState.COMPLETED,version=RoutingkeyVersions.V1)
            ic(res)
            return SuccessMessagingTypDict(
                response=res,
                emit_success=True,
                emit_payload=EventPublishingTypDict(
                    exchange_name="accounts.employees.employees.exchange",
                    routing_key=r_key,payload={},headers={'saga_id':self.saga_id}
                ),
                set_response=True,
                mark_completed=False
            )

  
    async def update(self)->SuccessMessagingTypDict:
        async with AsyncAccountDbLocalSession() as session:
            event_data:dict=self.payload['data']
            employees_data:dict=event_data.get("employees")
            ic(employees_data)

            if not employees_data:
                raise BussinessError(
                    type=ErrorTypeSEnum.BUSSINESS_ERROR,
                    error=SagaStateErrorTypDict(
                        code=ErrorTypeSEnum.BUSSINESS_ERROR.value,
                        debug="There is not accounts or employee data found on the payload",
                        user_msg="Something went wrong, please try again"
                    )
                )
            
            ic(f"Create : Headers=> {self.headers}, Payload => {self.payload} ")
            ic(not employees_data.get('account_id'))
            if employees_data.get('account_id',None) is None:
                raise BussinessError(
                    type=ErrorTypeSEnum.BUSSINESS_ERROR,
                    error=SagaStateErrorTypDict(
                        code=ErrorTypeSEnum.BUSSINESS_ERROR.value,
                        debug="Invalid payload for getting accounts info (email,account_id,mobile_number)",
                        user_msg="Invalid payload for accounts from user"
                    )
                )
            
            res=await AccountService(session=session).getby_id(account_id=employees_data.get('account_id'),timezone=TimeZoneEnum.Asia_Kolkata)
            ic(res)
            if not res or len(res)<1:
                raise BussinessError(
                    type=ErrorTypeSEnum.BUSSINESS_ERROR,
                    error=SagaStateErrorTypDict(
                        code=ErrorTypeSEnum.BUSSINESS_ERROR.value,
                        debug="Account service could not be able to find a account for the given account id",
                        user_msg="Invalid payload for accounts, from user"
                    )
                )
            
            res={
                'account_id':res['id'],
                'name':res['name'],
                'mobile_number':res['mobile_number'],
                'email':res['email'],
            }
            
            r_key=generate_routingkey(domain="accounts",work_for="employees",action=RoutingkeyActions.UPDATE,state=RoutingkeyState.COMPLETED,version=RoutingkeyVersions.V1)
            return SuccessMessagingTypDict(
                response=res,
                emit_success=True,
                emit_payload=EventPublishingTypDict(
                    exchange_name="accounts.employees.employees.exchange",routing_key=r_key,payload={},headers={'saga_id':self.saga_id}
                ),
                set_response=True,
                mark_completed=False
            )
        
    
    async def revoke(self)->SuccessMessagingTypDict:
        async with AsyncAccountDbLocalSession() as session:
            ic(f"Create : Headers=> {self.headers}, Payload => {self.payload} ")
            event_data:dict=self.payload['data']
            accounts_data:dict=event_data.get("accounts")
            if not accounts_data:
                raise BussinessError(
                    type=ErrorTypeSEnum.BUSSINESS_ERROR,
                    error=SagaStateErrorTypDict(
                        code=ErrorTypeSEnum.BUSSINESS_ERROR.value,
                        debug="There is not accounts or employee data found on the payload",
                        user_msg="Something went wrong, please try again"
                    )
                )
            if not accounts_data['id']:
                raise BussinessError(
                    type=ErrorTypeSEnum.BUSSINESS_ERROR,
                    error=SagaStateErrorTypDict(
                        code=ErrorTypeSEnum.BUSSINESS_ERROR.value,
                        debug="Account revocation, there is no account id presents",
                        user_msg="No account-id found"
                    )
                )
            res=await AccountService(session=session).delete(account_id=accounts_data['id'])
            if not res:
                raise BussinessError(
                    type=ErrorTypeSEnum.BUSSINESS_ERROR,
                    error=SagaStateErrorTypDict(
                        code=ErrorTypeSEnum.BUSSINESS_ERROR.value,
                        debug="Account revocation failed due to invalid account id ",
                        user_msg="Invalid account-id for revoking accounts"
                    )
                )
            
            return SuccessMessagingTypDict(
                response=res,
                mark_completed=False
            )
    
    async def delete(self):
        ...
