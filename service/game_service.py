from typing import Dict, Any

from ai_api.api_client import ChatSession
from config.decorators import get_config_manager, config_value
from service.story_service import init_attributes


class GameControl:
    def __init__(self):
        self.configmanager = get_config_manager()
        self.minT = self.require_story("")
        init_attributes(self.configmanager)

    def require_story(self, key):
        return self.configmanager.get_story_value(key)