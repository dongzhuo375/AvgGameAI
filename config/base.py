from typing import Any, Dict, Optional

from config.loaders import ConfigLoader


class BaseConfig:
    """基础配置类 - 封装通用功能"""

    def __init__(self, loader: ConfigLoader):
        self._loader = loader
        self._data: Dict[str, Any] = {}
        self._current_file: Optional[str] = None

    def load(self, file_path: str) -> bool:
        """加载配置文件"""
        self._current_file = file_path
        return self.reload()

    def reload(self) -> bool:
        """重新加载当前配置文件"""
        if not self._current_file or not self._loader:
            return False

        try:
            self._data = self._loader.load(self._current_file)
            print(f"配置加载成功: {self._current_file}")
            return True
        except Exception as e:
            print(f"配置加载失败: {e}")
            return False

    def get_value(self, key: str, default: Any = None) -> Any:
        """获取配置值（支持点分隔的嵌套键）"""
        keys = key.split('.')
        value = self._data

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def set_loader(self, loader: ConfigLoader):
        """动态设置加载器"""
        self._loader = loader

    def current_file(self) -> Optional[str]:
        """获取当前配置文件路径"""
        return self._current_file

    def get_all_data(self) -> Dict[str, Any]:
        """获取所有配置数据"""
        return self._data.copy()

    def has_key(self, key: str) -> bool:
        """检查配置键是否存在"""
        return self.get_value(key) is not None

    def get_int(self, key: str, default: int = 0) -> int:
        """获取整型配置值"""
        value = self.get_value(key, default)
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def get_float(self, key: str, default: float = 0.0) -> float:
        """获取浮点型配置值"""
        value = self.get_value(key, default)
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    def get_bool(self, key: str, default: bool = False) -> bool:
        """获取布尔型配置值"""
        value = self.get_value(key, default)
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 'on')
        return bool(value)
