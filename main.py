import asyncio
import os
from dotenv import load_dotenv
from meshview import web

async def main():
    # Load environment variables from .env file
    load_dotenv()

    # Read configuration from environment variables
    bind_address = os.getenv("BIND_ADDRESS")
    static_path = os.getenv("STATIC_PATH")

    # Ensure required environment variables are set
    required_vars = [bind_address, static_path]
    if not all(required_vars):
        print("Error: Missing required environment variables.")
        exit(1)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(
            web.run_server(bind_address, static_path)
        )

if __name__ == '__main__':
    asyncio.run(main())
