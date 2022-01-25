import logging
from aio_pika import connect

from .config import settings

logger = logging.getLogger(__name__)

async def connect_to_queue(loop, flow):

    if settings.MESSAGE_BROKER != None:
    
        connection = await connect(f"amqp://guest:guest@{settings.MESSAGE_BROKER}/", loop = loop)

        async with connection:

            exchange = 'MLBlock'
            queue_name = "jsons"
            routing_key = exchange+'.'+queue_name
        
            channel = await connection.channel()

            exchange = await channel.declare_exchange(exchange, type = "fanout")

            queue = await channel.declare_queue(queue_name)

            await queue.bind(exchange, routing_key)

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        logger.info(message.body)

                        if queue.name in message.body.decode():
                            break