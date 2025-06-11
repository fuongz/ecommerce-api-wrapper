import string
import random
import secrets
import time


class Faker:
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
        return f"d3d3LnRva29wZWRpYS5jb20=.{second_part}.{round(time.time())}"

    @staticmethod
    def user_agent():
        return random.choice(
            [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36",
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:39.0) Gecko/20100101 Firefox/39.0",
                "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; MASAJS; rv:11.0) like Gecko",
            ]
        )
