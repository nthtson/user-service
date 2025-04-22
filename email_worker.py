import json
import os

import pika
import requests

from config import DevelopmentConfig, ProductionConfig

config_class = (
    DevelopmentConfig if os.getenv("FLASK_ENV") == "development" else ProductionConfig
)


def send_email_via_mailtrap(
    to_email: str, full_name: str, subject: str, body: str
) -> None:
    headers = {
        "Authorization": f"Bearer {config_class.MAILTRAP_API_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "from": {
            "email": config_class.MAILTRAP_SENDER_EMAIL,
            "name": config_class.MAILTRAP_SENDER_NAME,
        },
        "to": [{"email": to_email, "name": full_name}],
        "subject": subject,
        "html": body,
        "text": body,
    }

    response = requests.post(
        config_class.MAILTRAP_API_URL, headers=headers, json=payload
    )

    if response.status_code != 200:
        print(f"[MAILTRAP ERROR] {response.status_code}: {response.text}")
    else:
        print(f"[MAILTRAP SUCCESS] Email sent to {to_email}")


def callback(ch, method, properties, body: bytes) -> None:
    try:
        message = json.loads(body)
        print(f"[WORKER] Received message: {message}")

        to_email = message.get("to_email")
        full_name = message.get("full_name")
        subject = message.get("subject", "Notification")
        body = message.get("body", "")

        if to_email:
            send_email_via_mailtrap(to_email, full_name, subject, body)
        else:
            print("[WORKER ERROR] 'to_email' missing in message")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"[WORKER ERROR] Failed to process message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)


def main() -> None:
    connection = pika.BlockingConnection(pika.URLParameters(config_class.RABBITMQ_URL))
    channel = connection.channel()
    channel.queue_declare(queue=config_class.EMAIL_QUEUE_NAME, durable=True)
    print("[WORKER] Waiting for messages. To exit press CTRL+C")

    channel.basic_consume(
        queue=config_class.EMAIL_QUEUE_NAME, on_message_callback=callback
    )
    channel.start_consuming()


if __name__ == "__main__":
    main()
