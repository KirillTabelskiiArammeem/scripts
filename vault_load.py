import hvac
from hvac.adapters import JSONAdapter
import os
from collections import namedtuple
import json
import time
from threading import RLock




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
        return super().request(*args, **kwargs)


Path = namedtuple("Path", ["application", "infrastructure", "security"])

VAULT_ADDR = os.getenv("VAULT_ADDR", "http://vault:8200")
VAULT_TIMEOUT = os.getenv("VAULT_TIMEOUT", 30)
VAULT_NAMESPACE = os.getenv("VAULT_NAMESPACE")
VAULT_MOUNT_POINT = os.getenv("VAULT_MOUNT_POINT", "bss")
VAULT_DEFAULT_ENGINE = os.getenv("VAULT_DEFAULT_ENGINE", "kv")
VAULT_TOKEN = os.getenv("VAULT_TOKEN")
VAULT_JWT_LOGIN_PATH = os.getenv("VAULT_JWT_LOGIN_PATH", "v1/auth/erpdev/login")
VAULT_JWT_TOKEN = os.getenv("VAULT_JWT_TOKEN")
VAULT_JWT_TOKEN_FILE = os.getenv(
    "VAULT_JWT_TOKEN_FILE", "/run/secrets/kubernetes.io/serviceaccount/token"
)
VAULT_ROLE = os.getenv("VAULT_ROLE")

VAULT_PATH_PREFIX = VAULT_NAMESPACE or "data"

PATH = Path(
    application=f"{VAULT_PATH_PREFIX}/applications",
    infrastructure=f"{VAULT_PATH_PREFIX}/infrastructure",
    security=f"{VAULT_PATH_PREFIX}/security",
)


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
    client.kv.reads_secret_cersion(PATH.application, mount_point=VAULT_MOUNT_POINT)

def load_get():
    vault = get_vault()
