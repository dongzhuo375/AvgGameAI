import os
from types import SimpleNamespace
from typing import Any

from config.config_manager import ConfigManager

_stories_path : str = None
_end_text : str = None

_game_attributes : SimpleNamespace = None



def get_stories(newest_first=True):
    stories_path = _stories_path
    filenames = []

    if not os.path.exists(stories_path):
        print(f"错误：目录 '{stories_path}' 不存在")
        return filenames

    file_info = []
    for filename in os.listdir(stories_path):
        file_path = os.path.join(stories_path, filename)
        if (os.path.isfile(file_path) and
                (filename.endswith('.yaml') or filename.endswith('.yml'))):
            name_without_extension = os.path.splitext(filename)[0]
            mtime = os.path.getmtime(file_path)
            file_info.append((name_without_extension, mtime, filename))

    file_info.sort(key=lambda x: x[1], reverse=newest_first)
    filenames = [name for name, mtime, filename in file_info]

    return filenames

def set_storise_path(file: str):
    global _stories_path
    _stories_path = file

def get_stories_path():
    return  _stories_path

def set_end_text(text: str):
    global _end_text
    _end_text = text

def get_end_text():
    return  _end_text




def get(attr_name: str, default: Any = None) -> Any:
    """通过字符串获取属性值"""
    if _game_attributes is None:
        raise ValueError("属性尚未初始化，请先调用 GameControl.init_attributes()")
    return getattr(_game_attributes, attr_name, default)


def set(attr_name: str, value: Any):
    """通过字符串设置属性值"""
    global _game_attributes
    if _game_attributes is None:
        raise ValueError("属性尚未初始化，请先调用 GameControl.init_attributes()")
    setattr(_game_attributes, attr_name, value)


def init_attributes(configmanager: ConfigManager):
    global _game_attributes
    _game_attributes = None
    attributes_dict = configmanager.get_story_value("attributes")
    value_dict = {}
    for attr_name, attr_data in attributes_dict.items():
        if isinstance(attr_data, dict) and "value" in attr_data:
            value_dict[attr_name] = attr_data["value"]
        else:
            # 如果属性不是字典或没有value字段，直接使用原值
            value_dict[attr_name] = attr_data
    _game_attributes = SimpleNamespace(**value_dict)
