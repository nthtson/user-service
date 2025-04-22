import json

import pika

from app.v1.schemas.email_schema import EmailMessage


class EmailPublisher:
    def __init__(self, rabbitmq_url: str):
        self.rabbitmq_url = rabbitmq_url

    def publish_email(self, message: EmailMessage) -> None:
        connection = pika.BlockingConnection(pika.URLParameters(self.rabbitmq_url))
        channel = connection.channel()
        channel.queue_declare(queue="email_queue", durable=True)

        channel.basic_publish(
            exchange="",
            routing_key="email_queue",
            body=json.dumps(message.__dict__),
            properties=pika.BasicProperties(delivery_mode=2),
        )

        connection.close()
