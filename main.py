import os
import tkinter as tk
from tkinter import ttk

from config.config_manager import ConfigManager
from config.decorators import set_config_manager
from gui.base_ui import BaseUI
from gui.start_menu import StartMenuFrame
from gui.game_screen import GameScreenFrame
from gui.end_screen import EndScreenFrame
from service.story_service import set_storise_path


class MainApp(BaseUI):
    def __init__(self):
        super().__init__()
        self.title("AVG 游戏")
        self.geometry("1280x720")
        self.resizable(True, True)
        
        # 创建主容器,初始帧
        self.container = tk.Frame(self, bg='black')
        self.container.pack(fill=tk.BOTH, expand=True)

        self.frames = {}

        self.init_frames()

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

        if hasattr(frame, 'on_show'):
            frame.on_show()

def main():
    #初始化配置
    config_manager = ConfigManager()

    config_dir = os.path.join(os.path.dirname(__file__))
    global_config_path = os.path.join(config_dir, "config.json")

    config_manager.setup_global_config(global_config_path)
    set_config_manager(config_manager)
    set_storise_path(os.path.join(os.path.dirname(__file__), "data","stories"))

    app = MainApp()
    app.mainloop()

if __name__ == "__main__":
    main()