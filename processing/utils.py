from enum import Enum

class ReturnCodesMQTT():
    MESSAGES = {
        "0" : "Connection successful",
        "1" : "Connection refused – incorrect protocol version",
        "2" : "Connection refused – invalid client identifier",
        "3" : "Connection refused – server unavailable",
        "4" : "Connection refused – bad username or password",
        "5" : "Connection refused – not authorised",
        "6" : "Currently unused"
    }

    @classmethod
    def get_message(cls, code_rc):
        if code_rc > 5:
            code_rc = 6
        return cls.MESSAGES[str(code_rc)]
