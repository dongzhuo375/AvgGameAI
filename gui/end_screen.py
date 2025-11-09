import tkinter as tk
from tkinter import ttk
from .base_ui import BaseFrame, TypewriterLabel, RoundedBorderFrame

class EndScreenFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.result = None
        
        # 结束文本
        self.default_end_text = """故事结束了，但这只是你冒险旅程的一个节点。
        
在这个广阔的世界中，还有无数的秘密等待着你去发现，
还有更多的挑战等待着你去面对。

也许在不久的将来，你会再次回到这里，
开启一段全新的传奇故事...

感谢你的游玩！"""
        
        # 创建主框架
        self.main_frame = tk.Frame(self, bg='black')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 空白区域
        self.top_spacer = tk.Frame(self.main_frame, bg='black', height=50)
        self.top_spacer.pack(fill=tk.X)
        
        # 结束文本区域
        self.text_frame = RoundedBorderFrame(
            self.main_frame,
            border_width=2,
            border_color='white',
            radius=15,
            padding=5,
            bg='black'
        )
        self.text_frame.pack(fill=tk.BOTH, expand=True, padx=50)

        self.text_content = tk.Frame(self.text_frame, bg='black')
        self.text_content.pack(fill='both', expand=True, padx=15, pady=15)
        
        # 结束文本标签
        self.end_label = TypewriterLabel(
            self.text_content,
            style='Dialog.TLabel',
            background='black',
            foreground='white',
            font=('微软雅黑', 12),
            justify=tk.LEFT
        )
        self.end_label.pack(fill=tk.BOTH, expand=True)
        
        # 按钮区域
        self.button_frame = tk.Frame(self.main_frame, bg='black')
        self.button_frame.pack(fill=tk.X, pady=30)

        self.restart_button = ttk.Button(
            self.button_frame,
            text="重新开始",
            style='Game.TButton',
            command=self.on_restart
        )
        self.restart_button.pack(side=tk.LEFT, padx=(200, 10), ipadx=10, ipady=5)

        self.quit_button = ttk.Button(
            self.button_frame,
            text="退出游戏",
            style='Game.TButton',
            command=self.on_quit
        )
        self.quit_button.pack(side=tk.LEFT, padx=(10, 200), ipadx=10, ipady=5)
        
        # 初始禁用按钮
        self.restart_button.config(state='disabled')
        self.quit_button.config(state='disabled')
        
        # 存储基础尺寸
        self.base_top_spacer_height = 50
        self.base_text_frame_padx = 50
        self.base_button_frame_pady = 30
        self.base_restart_button_padx = (200, 10)
        self.base_quit_button_padx = (10, 200)
        self.base_button_ipadx = 10
        self.base_button_ipady = 5
        
    def apply_frame_resize(self, width, height):
        width_ratio = width / self.base_width
        height_ratio = height / self.base_height
        scale = min(width_ratio, height_ratio)
        
        # 调整结束标签字体大小
        self.end_label.update_font_size(scale)
        
        # 调整上方空白区域高度
        top_spacer_height = max(int(self.base_top_spacer_height * scale), 20)
        self.top_spacer.config(height=top_spacer_height)
        
        # 调整文本区域边距
        text_frame_padx = max(int(self.base_text_frame_padx * scale), 20)
        self.text_frame.pack_configure(padx=text_frame_padx)
        
        # 调整按钮区域边距
        button_frame_pady = max(int(self.base_button_frame_pady * scale), 15)
        self.button_frame.pack_configure(pady=button_frame_pady)
        
        # 调整内容区域边距
        content_pad_x = max(int(15 * scale), 5)
        content_pad_y = max(int(15 * scale), 5)
        self.text_content.pack_configure(padx=content_pad_x, pady=content_pad_y)
        
        # 调整按钮边距和内边距
        restart_padx_first = max(int(self.base_restart_button_padx[0] * scale), 50)
        restart_padx_second = max(int(self.base_restart_button_padx[1] * scale), 5)
        
        quit_padx_first = max(int(self.base_quit_button_padx[0] * scale), 5)
        quit_padx_second = max(int(self.base_quit_button_padx[1] * scale), 50)
        
        button_ipadx = max(int(self.base_button_ipadx * scale), 5)
        button_ipady = max(int(self.base_button_ipady * scale), 2)
        
        self.restart_button.pack_configure(
            padx=(restart_padx_first, restart_padx_second), 
            ipadx=button_ipadx, 
            ipady=button_ipady
        )
        self.quit_button.pack_configure(
            padx=(quit_padx_first, quit_padx_second), 
            ipadx=button_ipadx, 
            ipady=button_ipady
        )
        
    def on_show(self, end_text=None):
        """当界面显示时调用"""
        # 重置文本显示
        self.end_label.config(text="")

        self.restart_button.config(state='disabled')
        self.quit_button.config(state='disabled')
        
        # 使用传入的结束文本或默认文本
        text_to_display = end_text if end_text is not None else self.default_end_text

        self.end_label.typewriter_effect(text_to_display, delay=30, callback=self.enable_buttons)
        
    def enable_buttons(self):
        """启用按钮"""
        self.restart_button.config(state='normal')
        self.quit_button.config(state='normal')
        
    def on_restart(self):
        """重新开始游戏"""
        self.controller.show_frame("StartMenuFrame")
        
    def on_quit(self):
        """退出游戏"""
        self.controller.on_closing()