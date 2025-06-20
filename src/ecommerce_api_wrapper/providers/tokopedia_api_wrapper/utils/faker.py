import string
import random
import secrets
import time


class TokopediaFaker:
    @staticmethod
    def unique_id():
        return secrets.token_hex(32 // 2)

    @staticmethod
    def device_id():
        chars = string.ascii_letters + string.digits
        random_str = "".join(random.choice(chars) for _ in range(8))
        hex_str = random_str.encode("ascii").hex()
        decimal_token = int(hex_str, 16)
        return str(decimal_token)

    @staticmethod
    def iris_session_id():
        second_part = secrets.token_hex(16)
        # "www.tokopedia.com" ---b64encode---> "d3d3LnRva29wZWRpYS5jb20="
        base64_part = "d3d3LnRva29wZWRpYS5jb20="
        current_time = round(time.time())
        return f"{base64_part}.{second_part}.{current_time}"
