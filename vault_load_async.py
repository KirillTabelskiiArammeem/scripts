import os
import asyncio
import datetime
from collections import namedtuple
import async_hvac

Path = namedtuple("Path", ["application", "infrastructure", "security"])

VAULT_ADDR = os.getenv("VAULT_ADDR", "https://bss-vault.stg.toyou.amhub.org/")
VAULT_TIMEOUT = os.getenv("VAULT_TIMEOUT", 30)
VAULT_NAMESPACE = os.getenv("VAULT_NAMESPACE", 'am-mcp-12-sand')
VAULT_MOUNT_POINT = os.getenv("VAULT_MOUNT_POINT", "bss")
VAULT_DEFAULT_ENGINE = os.getenv("VAULT_DEFAULT_ENGINE", "kv")
VAULT_TOKEN = os.getenv("VAULT_TOKEN")
VAULT_JWT_LOGIN_PATH = os.getenv("VAULT_JWT_LOGIN_PATH", "v1/auth/erpdev/login")
VAULT_JWT_TOKEN_FILE = os.getenv(
    "VAULT_JWT_TOKEN_FILE", "./token"
)
VAULT_ROLE = os.getenv("VAULT_ROLE", 'am-mcp-12-sand')

VAULT_PATH_PREFIX = VAULT_NAMESPACE or "data"

PATH = Path(
    application=f"{VAULT_PATH_PREFIX}/applications",
    infrastructure=f"{VAULT_PATH_PREFIX}/infrastructure",
    security=f"{VAULT_PATH_PREFIX}/security",
)

with open(VAULT_JWT_TOKEN_FILE, "r") as f:
    VAULT_JWT_TOKEN = f.read().strip()

CLIENTS = []
async def get_client():
    client = async_hvac.AsyncClient(url=VAULT_ADDR, timeout=120)
    CLIENTS.append(client)

    response = await client._put(
        url=VAULT_JWT_LOGIN_PATH,
        headers = {
            "X-Vault-Request": "true",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            'jwt': VAULT_JWT_TOKEN,
            'role': VAULT_ROLE,
        }
    )
    response = await response.json()
    client.token = response['auth']['client_token']
    CLIENTS.append(client)
    return client

async def get_key(client):
    await client._get(url=f'/v1/{VAULT_MOUNT_POINT}/data/{VAULT_NAMESPACE}/applications')

PAUSE = 1

async def get_key_processor(client: async_hvac.AsyncClient, queue: asyncio.Queue):
    while True:
        message = await queue.get()
        if message is None:
            await queue.put(None)
        try:
            if PAUSE:
                await asyncio.sleep(PAUSE)
            await get_key(client)

        except Exception as er:
            print(f'finished with error {er}')
            raise er


CLIENTS_NUMBER = 500
TOTAL_MESSAGES = CLIENTS_NUMBER * 100


async def main():
    global TOTAL_MESSAGES
    await asyncio.gather(*[get_client() for _ in range(CLIENTS_NUMBER)])
    print('started')
    start = datetime.datetime.now()
    queue = asyncio.Queue()
    for i in range(TOTAL_MESSAGES):
        await queue.put(i)
    await queue.put(None)
    try:
        await asyncio.gather(*[get_key_processor(client, queue,) for client in CLIENTS])
    except Exception as er:
        TOTAL_MESSAGES = TOTAL_MESSAGES - queue.qsize()
    # for i in range(1, N + 1):
    #     sub_start = datetime.datetime.now()
    #     print(i)
    #     await asyncio.gather(*[get_key(client) for client in CLIENTS])
    #     sub_work_time = datetime.datetime.now() - sub_start
    #     print(sub_work_time, M / sub_work_time.total_seconds())

    for client in CLIENTS:
        await client.close()

    work_time = (datetime.datetime.now() - start).total_seconds()
    print(f'{work_time=}')
    print(f'{TOTAL_MESSAGES=}')
    RPS = TOTAL_MESSAGES / work_time
    print(f'{RPS=}')
    print(f'{PAUSE=}')


asyncio.run(main())
