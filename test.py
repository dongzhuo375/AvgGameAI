import os
import sys

sys.path.insert(0, os.path.abspath("."))

from config.config_loader import load_config
from ai_api.api_client import AIClient
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
    try:
        config = load_config()
        print("Config:", config)
    except Exception as e:
        print("读取出错:", e)

def test_api():
    print("测试AI模型API调用...")
    try:
        ai = AIClient()
        result = ai.send("你好，AI！")
        print("API返回:", result)
    except Exception as e:
        print("API调用出错:", e)

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


if __name__ == "__main__":
    print("=== 功能测试 ===")
    test_config()
    test_api()
    test_audio()
    test_start_menu()  # 启动实际的开始菜单界面
    print("=== 测试结束 ===")