def validate_config(config):
    required_keys = [
        "USERNAME",
        "PASSWORD",
        "auth_url",
        "device_url",
        "data_url",
        "measurements",
    ]
    missing = [key for key in required_keys if not config.get(key)]
    if missing:
        raise ValueError(f"Missing required config keys: {missing}")
    return config
