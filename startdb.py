import asyncio
import argparse
import os
from dotenv import load_dotenv
from meshview import mqtt_reader
from meshview import mqtt_database
from meshview import mqtt_store
import json


async def load_database_from_mqtt(mqtt_server: str , mqtt_port: int, topic: list, mqtt_user: str | None = None, mqtt_passwd: str | None = None):
    async for topic, env in mqtt_reader.get_topic_envelopes(mqtt_server, mqtt_port, topic, mqtt_user, mqtt_passwd):
        await mqtt_store.process_envelope(topic, env)


async def main():
    # Load environment variables from .env file
    load_dotenv()

    # Read configuration from environment variables
    db_connection_string = os.getenv("DATABASE_CONNECTION_STRING")
    mqtt_server = os.getenv("MQTT_SERVER")
    mqtt_port = os.getenv("MQTT_PORT")
    mqtt_topics = os.getenv("MQTT_TOPICS")
    mqtt_user = os.getenv("MQTT_USERNAME")
    mqtt_passwd = os.getenv("MQTT_PASSWORD")

    # Ensure required environment variables are set
    required_vars = [db_connection_string, mqtt_server, mqtt_port, mqtt_topics]
    if not all(required_vars):
        print("Error: Missing required environment variables.")
        exit(1)

    mqtt_database.init_database(db_connection_string)
    await mqtt_database.create_tables()

    mqtt_topics = json.loads(mqtt_topics)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(
            load_database_from_mqtt(mqtt_server, int(mqtt_port), mqtt_topics, mqtt_user, mqtt_passwd)
        )


if __name__ == '__main__':
    asyncio.run(main())
