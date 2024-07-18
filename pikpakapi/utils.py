import hashlib
from uuid import uuid4
import time

CLIENT_ID = "YNxT9w7GMdWvEOKa"
CLIENT_SECRET = "dbw2OtmVEeuUvIptb1Coyg"
CLIENT_VERSION = "1.46.2"
PACKAG_ENAME = "com.pikcloud.pikpak"
SDK_VERSION = "2.0.4.204000 "
APP_NAME = PACKAG_ENAME


def get_timestamp() -> int:
    """
    Get current timestamp.
    """
    return int(time.time() * 1000)


def device_id_generator() -> str:
    """
    Generate a random device id.
    """
    return str(uuid4()).replace("-", "")


SALTS = [
    "PAe56I7WZ6FCSkFy77A96jHWcQA27ui80Qy4",
    "SUbmk67TfdToBAEe2cZyP8vYVeN",
    "1y3yFSZVWiGN95fw/2FQlRuH/Oy6WnO",
    "8amLtHJpGzHPz4m9hGz7r+i+8dqQiAk",
    "tmIEq5yl2g/XWwM3sKZkY4SbL8YUezrvxPksNabUJ",
    "4QvudeJwgJuSf/qb9/wjC21L5aib",
    "D1RJd+FZ+LBbt+dAmaIyYrT9gxJm0BB",
    "1If",
    "iGZr/SJPUFRkwvC174eelKy",
]


def captcha_sign(device_id: str, timestamp: str) -> str:
    """
    Generate a captcha sign.

    在网页端的js中, 搜索 captcha_sign, 可以找到对应的js代码

    """
    sign = CLIENT_ID + CLIENT_VERSION + PACKAG_ENAME + device_id + timestamp
    for salt in SALTS:
        sign = hashlib.md5((sign + salt).encode()).hexdigest()
    return f"1.{sign}"


def generate_device_sign(device_id, package_name):
    signature_base = f"{device_id}{package_name}1appkey"

    # 计算 SHA-1 哈希
    sha1_hash = hashlib.sha1()
    sha1_hash.update(signature_base.encode("utf-8"))
    sha1_result = sha1_hash.hexdigest()

    # 计算 MD5 哈希
    md5_hash = hashlib.md5()
    md5_hash.update(sha1_result.encode("utf-8"))
    md5_result = md5_hash.hexdigest()

    device_sign = f"div101.{device_id}{md5_result}"

    return device_sign


def build_custom_user_agent(device_id, user_id):
    device_sign = generate_device_sign(device_id, PACKAG_ENAME)

    user_agent_parts = [
        f"ANDROID-{APP_NAME}/{CLIENT_VERSION}",
        "protocolVersion/200",
        "accesstype/",
        f"clientid/{CLIENT_ID}",
        f"clientversion/{CLIENT_VERSION}",
        "action_type/",
        "networktype/WIFI",
        "sessionid/",
        f"deviceid/{device_id}",
        "providername/NONE",
        f"devicesign/{device_sign}",
        "refresh_token/",
        f"sdkversion/{SDK_VERSION}",
        f"datetime/{get_timestamp()}",
        f"usrno/{user_id}",
        f"appname/{APP_NAME}",
        "session_origin/",
        "grant_type/",
        "appid/",
        "clientip/",
        "devicename/Xiaomi_M2004j7ac",
        "osversion/13",
        "platformversion/10",
        "accessmode/",
        "devicemodel/M2004J7AC",
    ]

    return " ".join(user_agent_parts)
