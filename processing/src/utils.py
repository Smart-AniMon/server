from enum import Enum
import binascii

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

def str64_to_bytes(image_base64: str) -> bytes:
    image_base64_bytes = image_base64.encode('utf-8')    # string to bytes code base64
    image_bytes = binascii.a2b_base64(image_base64_bytes) # decode base64    
    return  image_bytes

def get_name(c : object) -> str:
    return c.__module__+'.'+c.__class__.__name__

def check_labels(label: str, labels: list) -> bool:
    for description in labels:
        if description.upper() in label:
            return True
    return False

