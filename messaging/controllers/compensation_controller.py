from aio_pika.abc import AbstractIncomingMessage
from dataclasses import dataclass
from typing import List
from hyperlocal_platform.core.enums.routingkey_enum import RoutingkeyActions

@dataclass(frozen=True)
class CompensationController:
    msg:AbstractIncomingMessage

    def decide(self,saga_payload:dict)->bool:
        routing_key:str=self.msg.routing_key
        domain,work_for,action,state,version=routing_key.split('.')

        key:str=f"{domain}.{action}"

        if domain=='employees':
                return False
        
        return False
