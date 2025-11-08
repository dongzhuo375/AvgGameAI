"""
配置装饰器
"""

import functools
from typing import Any, Callable, Optional

from config.config_manager import ConfigManager

# 全局配置管理器实例
_config_manager: Optional['ConfigManager'] = None

def get_config_manager() -> 'ConfigManager':
    """获取配置管理器实例"""
    global _config_manager
    if _config_manager is None:
        from config_manager import ConfigManager
        _config_manager = ConfigManager()
    return _config_manager


def set_config_manager(manager: 'ConfigManager'):
    """设置配置管理器实例"""
    global _config_manager
    _config_manager = manager


def config_value(config_key: str, default: Any = None, use_story: bool = False):
    """
    配置值注入装饰器
    自动将配置值注入到函数参数

    Args:
        config_key: 配置键（支持点分隔）
        default: 默认值
        use_story: 是否使用故事配置
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 获取配置管理器实例
            config_manager = get_config_manager()

            # 获取配置值
            if use_story:
                value = config_manager.get_story_value(config_key, default)
            else:
                value = config_manager.get_global_value(config_key, default)

            # 确定参数名（使用配置键的最后一部分）
            param_name = config_key.split('.')[-1]

            # 如果参数名不在kwargs中，则注入
            if param_name not in kwargs:
                kwargs[param_name] = value

            return func(*args, **kwargs)

        return wrapper

    return decorator


def require_config(config_key: str, use_story: bool = False):
    """
    要求配置存在的装饰器
    如果配置不存在，则抛出 ValueError

    Args:
        config_key: 配置键
        use_story: 是否使用故事配置
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            config_manager = get_config_manager()

            if use_story:
                value = config_manager.get_story_value(config_key)
            else:
                value = config_manager.get_global_value(config_key)

            if value is None:
                config_type = "故事" if use_story else "全局"
                raise ValueError(f"必需的{config_type}配置缺失: {config_key}")

            return func(*args, **kwargs)

        return wrapper

    return decorator