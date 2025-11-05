from config.config_manager import GlobalConfig


class ApiConfig:
    def __init__(self, global_config: GlobalConfig):
        self.global_config = global_config

    def get_key(self) -> str:
        return self.global_config.get("api_key")

    def get_url(self) -> str:
        return self.global_config.get("base_url")

    def get_timeout(self) -> int:
        return self.global_config.get("timeout")