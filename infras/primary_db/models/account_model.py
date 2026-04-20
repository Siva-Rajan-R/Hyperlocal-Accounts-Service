from ..main import BASE
from sqlalchemy import Column, String,ForeignKey,Integer,TIMESTAMP,func,Boolean,ARRAY,Identity,BigInteger


class Accounts(BASE):
    __tablename__="accounts"
    id=Column(String,primary_key=True)
    sequence_id=Column(BigInteger,Identity(always=True),nullable=False)
    name=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True)
    mobile_number=Column(String,nullable=True)
    source=Column(String,nullable=False)
    accessed=Column(ARRAY(String),nullable=True)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=func.now())
