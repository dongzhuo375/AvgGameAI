import os
import sys
import tempfile
import json

sys.path.insert(0, os.path.abspath("."))

from config.config_loader import JsonConfigLoader, YamlConfigLoader
from config.config_manager import GlobalConfig, StoryConfig
from ai_api.api_service import ApiConfig
from audio.audio_player import play_audio
from gui.start_menu import StartMenuFrame
from gui.game_screen import GameScreenFrame
from gui.end_screen import EndScreenFrame
import tkinter as tk
from gui.base_ui import BaseUI

class TestApp(BaseUI):
    def __init__(self):
        super().__init__()
        self.title("AVG 游戏测试")
        self.geometry("1280x720")
        self.resizable(True, True)
        
        # 创建主容器
        self.container = tk.Frame(self, bg='black')
        self.container.pack(fill=tk.BOTH, expand=True)
        
        # 存储所有界面帧
        self.frames = {}
        
        # 初始化所有界面
        self.init_frames()
        
        # 显示起始菜单
        self.show_frame("StartMenuFrame")
        
    def init_frames(self):
        for FrameClass in (StartMenuFrame, GameScreenFrame, EndScreenFrame):
            frame_name = FrameClass.__name__
            frame = FrameClass(parent=self.container, controller=self)
            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        # 配置网格权重
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()
        
        # 如果有特殊显示逻辑，调用相应方法
        if hasattr(frame, 'on_show'):
            frame.on_show()

def test_config():
    print("测试配置文件读取...")
    # 跳过此测试，因为我们将在test_global_config和test_story_config中测试配置加载

# def test_api():
#     print("测试AI模型API调用...")
#     try:
#         ai = AIClient()
#         result = ai.send("你好，AI！")
#         print("API返回:", result)
#     except Exception as e:
#         print("API调用出错:", e)

def test_audio():
    print("测试音频播放功能...")
    try:
        # 需先备一个resources/test.mp3或test.wav
        play_audio("resources/test.mp3")
        print("音频播放调用完成。")
    except Exception as e:
        print("播放出错:", e)

def test_start_menu():
    """测试启动开始菜单界面"""
    print("启动开始菜单界面测试...")
    try:
        app = TestApp()
        app.mainloop()
        print("开始菜单界面测试完成。")
    except Exception as e:
        print("界面启动出错:", e)

def test_config_loader_json():
    """测试JSON配置加载器"""
    print("测试JSON配置加载器...")
    loader = JsonConfigLoader()
    
    # 检查是否存在本地配置文件
    json_config_file = "aaa.json"
    if os.path.exists(json_config_file):
        try:
            loaded_data = loader.load(json_config_file)
            print(f"成功加载JSON配置文件: {json_config_file}")
            print("JSON配置加载器测试通过")
        except Exception as e:
            print(f"JSON配置加载器测试失败: {e}")
    else:
        print(f"未找到本地JSON配置文件: {json_config_file}，跳过测试")

def test_config_loader_yaml():
    """测试YAML配置加载器"""
    print("测试YAML配置加载器...")
    loader = YamlConfigLoader()
    
    # 检查是否存在本地配置文件
    yaml_config_file = "config/config.yaml"
    if os.path.exists(yaml_config_file):
        try:
            loaded_data = loader.load(yaml_config_file)
            print(f"成功加载YAML配置文件: {yaml_config_file}")
            print("YAML配置加载器测试通过")
        except Exception as e:
            print(f"YAML配置加载器测试失败: {e}")
    else:
        print(f"未找到本地YAML配置文件: {yaml_config_file}，跳过测试")

def test_global_config():
    """测试全局配置管理"""
    print("测试全局配置管理...")
    try:
        # 创建并注入加载器
        global_config = GlobalConfig(JsonConfigLoader())
        
        # 检查是否存在本地配置文件
        json_config_file = "aaa.json"
        if os.path.exists(json_config_file):
            # 初始化配置
            global_config.initialize(json_config_file)
            if global_config.is_initialized():
                print("全局配置管理初始化成功")
                # 尝试获取一些配置值（如果存在）
                api_key = global_config.get("api_key", "not_found")
                base_url = global_config.get("base_url", "not_found")
                timeout = global_config.get("timeout", -1)
                
                print(f"API Key: {api_key}")
                print(f"Base URL: {base_url}")
                print(f"Timeout: {timeout}")
                print("全局配置管理测试通过")
            else:
                print("全局配置管理初始化失败")
        else:
            print(f"未找到本地JSON配置文件: {json_config_file}，跳过测试")
    except Exception as e:
        print(f"全局配置管理测试失败: {e}")

def test_story_config():
    """测试故事配置管理"""
    print("测试故事配置管理...")
    try:
        # 创建并注入加载器
        story_config = StoryConfig(YamlConfigLoader())
        
        # 检查是否存在本地配置文件
        yaml_config_file = "config/story.yaml"
        if os.path.exists(yaml_config_file):
            # 加载配置
            result = story_config.load(yaml_config_file)
            if result:
                print("故事配置管理加载成功")
                # 尝试获取一些配置值（如果存在）
                title = story_config.get("title", "not_found")
                print(f"Story Title: {title}")
                print("故事配置管理测试通过")
            else:
                print("故事配置管理加载失败")
        else:
            print(f"未找到本地YAML配置文件: {yaml_config_file}，跳过测试")
    except Exception as e:
        print(f"故事配置管理测试失败: {e}")

def test_api_config():
    """测试API配置"""
    print("测试API配置...")
    try:
        # 创建模拟的GlobalConfig实例
        class MockGlobalConfig:
            def get(self, key, default=None):
                config_map = {
                    "api_key": "test_key_123",
                    "base_url": "https://api.test.com",
                    "timeout": 60
                }
                return config_map.get(key, default)
        
        mock_global_config = MockGlobalConfig()
        api_config = ApiConfig(mock_global_config)
        
        # 测试获取配置值
        assert api_config.get_key() == "test_key_123"
        assert api_config.get_url() == "https://api.test.com"
        assert api_config.get_timeout() == 60
        
        print("API配置测试通过")
    except Exception as e:
        print(f"API配置测试失败: {e}")

if __name__ == "__main__":
    print("=== 功能测试 ===")
    # test_config()
    test_config_loader_json()
    # test_config_loader_yaml()
    test_global_config()
    # test_story_config()
    # test_api_config()
    # test_api()
    # test_audio()
    # test_start_menu()
    print("=== 测试结束 ===")