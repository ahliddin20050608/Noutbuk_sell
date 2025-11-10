import re

def validate_fullname(name:str) -> bool:
    name = name.strip()
    pattern = r"^[A-Z][a-z]+(?:\s[A-Z][a-z]+)+$"
    return bool(re.match(pattern, name))


def validate_phone(phone:str) -> bool:
    phone = phone.strip().replace(" ", "")
    pattern = r"^\+998\d{9}$"
    return bool(re.match(pattern, phone))