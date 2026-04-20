# import aio_pika
# from aio_pika import RobustConnection,ExchangeType,Message,DeliveryMode
# from aio_pika.abc import AbstractIncomingMessage,HeadersType
# import orjson,asyncio


# # get_connection() -> create_excahnge() -> create_queues() -> publish_events() or consume_events()
# async def get_connection()->RobustConnection:
#     connection=await aio_pika.connect_robust()
#     return connection


# async def create_exchange(name:str,exchange_type:ExchangeType):
#     conn=await get_connection()
#     ch=await conn.channel()

#     exchange = await ch.declare_exchange(
#         name=name,
#         type=exchange_type,
#         durable=True
#     )

#     print(f"Exchange created successfully ✅ -> {exchange}")
#     return exchange 


# async def create_queue(routing_key:str,exchange_name:str,queue_name:str):
#     conn=await get_connection()
#     ch=await conn.channel()
#     queue=await ch.declare_queue(name=queue_name,durable=True)
#     await queue.bind(exchange=exchange_name,routing_key=routing_key)
#     print(f"Queue created successfully ✅ -> {queue}")
#     return queue


# async def publish_events(routing_key:str,payload:dict,headers:dict,exchange_name:str):
#     conn=await get_connection()
#     ch=await conn.channel()
#     exchange=await ch.get_exchange(name=exchange_name)
#     message=Message(
#         body=orjson.dumps(payload),
#         headers=headers,
#         delivery_mode=DeliveryMode.PERSISTENT
#     )
#     await exchange.publish(
#         message=message,
#         routing_key=routing_key
#     )
#     print("Event published successfully ✅")


# async def consume_events(queue_name:str,handler):
#     conn=await get_connection()
#     ch=await conn.channel()

#     queue=await ch.get_queue(name=queue_name)

#     await queue.consume(handler)

#     print(f"CONSUMING EVENTS OF -> {queue_name}")

#     await asyncio.Future()


# async def employee_handler(msg:AbstractIncomingMessage):
#     async with msg.process():
#         routing_key:str=msg.routing_key
#         headers:dict=msg.headers
#         payload:dict=orjson.loads(msg.body)
#         print(f"{routing_key}\n{headers}\n{payload}")

#         if routing_key=='employees.created':
#             print(f"Account created successfully -> {payload}")
#             print("Create it on READ-DB")
#             print("Publishing event")
#             await publish_events(
#                 routing_key="accounts.created",
#                 exchange_name='exchange.topic',
#                 payload={'name':'sivarajan R','email':'siva@gmail.com','mobile_number':'1234567890','account_id':'123-456'},
#                 headers={}
#             )

#         elif routing_key=="employees.updated":
#             print(f"Account updated successfully -> {payload}")
#             print("Update it on READ-DB")

#         elif routing_key=='employees.failed':
#             print(f"Account createation or updation failed -> {payload}")
            

# # 
# async def exchanges():
#     exchanges=[
#         {
#             'name':'exchange.direct',
#             'type':ExchangeType.DIRECT
#         },
#         {
#             'name':'exchange.topic',
#             'type':ExchangeType.TOPIC
#         }
#     ]

#     for exchange in exchanges:
#         await create_exchange(name=exchange['name'],exchange_type=exchange['type'])

# async def queues():
#     queues=[
#         {'r_key':'employees.*.v1','q_name':'employees.queue','ex_name':'exchange.topic'}
#     ]

#     for queue in queues:
#         await create_queue(routing_key=queue['r_key'],exchange_name=queue['ex_name'],queue_name=queue['q_name'])

# async def consumers():
#     consumers=[
#         {'q_name':'employees.queue','handler':employee_handler}
#     ]

#     for consumer in consumers:
#         await consume_events(queue_name=consumer['q_name'],handler=consumer['handler'])
# async def main():
#     await exchanges()
#     await queues()
#     await consumers()

# asyncio.run(main())

print(isinstance(4,str))