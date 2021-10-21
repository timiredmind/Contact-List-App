create_user_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "email": {"type": "string"},
        "password": {'type': "string"},
        "phone_number": {"type": "string"}
    },
    "required": ["username", "email", "password", "phone_number"]
}

login_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"}
    },
    "required": ["username", "password"]

}

patch_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "email": {"type": "string"},
        "phone_number": {"type": "string"}
    },
    "required": ["username", "email", "phone_number"]
}

contact_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "email": {"type": "string"},
        "phone_number": {"type": "string"},
        "address": {"type": "string"},
        "image_url": {"type": "string"}
    },
    "required": ["name", "email", "phone_number"]
}


