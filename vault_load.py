import io
import threading
import multiprocessing

import hvac
from hvac.adapters import JSONAdapter
import os
from collections import namedtuple
import json
import time
from threading import RLock
import datetime
import cProfile
import cProfile, pstats, io
from pstats import SortKey



class JwtJsonAdapter(JSONAdapter):
    def __init__(
        self,
        *args,
        jwt_token=None,
        jwt_auth_login_path="v1/auth/erpdev/login",
        vault_role=None,
        head_start=60,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.token_tll = 0
        self.auth_lock = RLock()
        self.jwt_token = jwt_token
        self.vault_role = vault_role

        self.jwt_auth_headers = {
            "X-Vault-Request": "true",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        self.jwt_auth_data = {
            "jwt": self.jwt_token,
            "role": self.vault_role,
        }
        self.jwt_auth_login_path = jwt_auth_login_path
        self.head_start = head_start

    def jwt_auth(self):
        with self.auth_lock:
            if time.time() <= self.token_tll:
                return
            response = self.put(
                self.jwt_auth_login_path,
                headers=self.jwt_auth_headers,
                data=json.dumps(self.jwt_auth_data),
                skip_auth=True,
            )
            self.token = response["auth"]["client_token"]
            lease_duration = response["auth"]["lease_duration"]
            lease_duration = (
                lease_duration - self.head_start
                if lease_duration > self.head_start
                else lease_duration
            )
            self.token_tll = lease_duration + int(time.time())

    def request(
        self,
        *args,
        skip_auth=False,
        **kwargs,
    ):
        if not skip_auth:
            self.jwt_auth()
        print(args, kwargs)
        return super().request(*args, **kwargs)


Path = namedtuple("Path", ["application", "infrastructure", "security"])

VAULT_ADDR = os.getenv("VAULT_ADDR", "https://bss-vault.stg.toyou.amhub.org/")
VAULT_TIMEOUT = os.getenv("VAULT_TIMEOUT", 30)
VAULT_NAMESPACE = os.getenv("VAULT_NAMESPACE", 'am-mcp-12-sand')
VAULT_MOUNT_POINT = os.getenv("VAULT_MOUNT_POINT", "bss")
VAULT_DEFAULT_ENGINE = os.getenv("VAULT_DEFAULT_ENGINE", "kv")
VAULT_TOKEN = os.getenv("VAULT_TOKEN")
VAULT_JWT_LOGIN_PATH = os.getenv("VAULT_JWT_LOGIN_PATH", "v1/auth/erpdev/login")
VAULT_JWT_TOKEN = os.getenv("VAULT_JWT_TOKEN")
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


THREADS = 1
REQUESTS = 100
PROCESSES = 100


def get_jwt_json_adapter(*args, **kwargs):

    vault_jwt_token = VAULT_JWT_TOKEN
    if vault_jwt_token is None:
        with open(VAULT_JWT_TOKEN_FILE) as jwt_token_file:
            vault_jwt_token = jwt_token_file.read().strip()

    return JwtJsonAdapter(
        *args,
        **kwargs,
        jwt_token=vault_jwt_token,
        jwt_auth_login_path=VAULT_JWT_LOGIN_PATH,
        vault_role=VAULT_ROLE,
    )


def get_vault():
    """
    Get vault client
    :return: hvac.Client
    """

    adapter = JSONAdapter if VAULT_TOKEN else get_jwt_json_adapter

    client = hvac.Client(
        url=VAULT_ADDR,
        timeout=VAULT_TIMEOUT,
        namespace=VAULT_NAMESPACE,
        adapter=adapter,
    )

    if VAULT_TOKEN:
        client.token = VAULT_TOKEN

    return client


def get_keys(client: hvac.Client):
    client.kv.read_secret_version(path=PATH.application, mount_point=VAULT_MOUNT_POINT, raise_on_deleted_version=False)


def get_keys_worker(client: hvac.Client, num):
    for i in range(num):
        get_keys(client)


def load_get():
    vault = get_vault()
    get_keys_worker(vault, REQUESTS)
    # threads = [threading.Thread(target=get_keys_worker, args=(vault, REQUESTS)) for _ in range(THREADS)]
    # [thread.start() for thread in threads]
    # [thread.join() for thread in threads]

def main():
    pr = cProfile.Profile()
    pr.enable()
    start = datetime.datetime.now()
    print(f'''
    Stare test
    REQUESTS: {REQUESTS}
    THREADS: {THREADS}
    PROCESSES: {PROCESSES}
    Total (REQUESTS * THREADS * PROCESSES): {REQUESTS * THREADS * PROCESSES}
    ''')

    load_get()
    processes = [multiprocessing.Process(target=load_get) for _ in range(PROCESSES)]
    [process.start() for process in processes]
    [process.join() for process in processes]
    worktime = datetime.datetime.now() - start
    worktime_seconds = worktime.total_seconds()
    print(f'processing time: {worktime_seconds} \nrps {REQUESTS * THREADS * PROCESSES / worktime_seconds}')
    pr.disable()
    s = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())

main()

