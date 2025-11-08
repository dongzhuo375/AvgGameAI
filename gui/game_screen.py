import tkinter as tk
from tkinter import ttk
from .base_ui import BaseFrame, TypewriterLabel, RoundedBorderFrame

class GameScreenFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        # 游戏对话文本示例
        self.dialog_text = "欢迎来到这个精彩的故事世界。在这里，你将体验一段难忘的冒险旅程..."
        
        # 选项文本示例
        self.choices = ["探索森林", "前往城镇", "休息一下"]

        self.is_typing = False
        self.text_finished = False  # 标记文本是否已完成显示
        
        # 创建主框架
        self.main_frame = tk.Frame(self, bg='black')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.main_frame.bind("<Button-1>", self.on_click)
        
        # 空白区域
        self.top_spacer = tk.Frame(self.main_frame, bg='black', height=100)
        self.top_spacer.pack(fill=tk.X)
        
        # 选项区域
        self.choice_frame = tk.Frame(self.main_frame, bg='black')
        # 不调用pack方法，保持隐藏状态

        self.choice_buttons = []
        for i, choice_text in enumerate(self.choices):
            button = ttk.Button(
                self.choice_frame,
                text=choice_text,
                style='Choice.TButton',
                command=lambda idx=i: self.on_choice(idx)
            )
            button.pack(pady=5, ipadx=20, ipady=5)
            self.choice_buttons.append(button)
        
        # 对话框区域
        self.dialog_frame = RoundedBorderFrame(
            self.main_frame,
            border_width=2,
            border_color='white',
            radius=15,
            padding=5,
            bg='black'
        )
        self.dialog_frame.pack(fill=tk.X, padx=50, pady=(0, 20), side=tk.BOTTOM)
        # 绑定鼠标事件
        self.dialog_frame.bind("<Button-1>", self.on_click)

        self.dialog_content = tk.Frame(self.dialog_frame, bg='black')
        self.dialog_content.pack(fill='both', expand=True, padx=15, pady=15)
        self.dialog_content.bind("<Button-1>", self.on_click)
        
        # 对话文本标签
        self.dialog_label = TypewriterLabel(
            self.dialog_content,
            style='Dialog.TLabel',
            background='black',
            foreground='white',
            font=('微软雅黑', 14),
            justify=tk.LEFT
        )
        self.dialog_label.pack(fill=tk.X, pady=(0, 5))
        self.dialog_label.bind("<Button-1>", self.on_click)

        self.indicator_label = tk.Label(
            self.dialog_content,
            text="▼",
            font=('微软雅黑', 16),
            bg='black',
            fg='white',
            anchor='e'
        )
        self.indicator_label.pack(fill=tk.X)
        self.indicator_label.bind("<Button-1>", self.on_click)

        self.base_top_spacer_height = 200
        self.base_dialog_padx = 50
        self.base_dialog_pady = 20
        self.base_choice_pady = (100, 20)
        self.base_dialog_label_pady = (0, 5)
        self.base_button_ipadx = 20
        self.base_button_ipady = 5
        
    def on_click(self, event):
        """处理鼠标点击事件"""
        if self.is_typing:
            self.dialog_label.skip_typewriter()
            self.is_typing = False
        elif self.text_finished:
            self.show_choices()
            self.text_finished = False 
        
    def apply_frame_resize(self, width, height):
        width_ratio = width / self.base_width
        height_ratio = height / self.base_height
        scale = min(width_ratio, height_ratio)
        
        # 调整对话标签字体大小
        self.dialog_label.update_font_size(scale)

        top_spacer_height = max(int(self.base_top_spacer_height * scale), 20)
        self.top_spacer.config(height=top_spacer_height)
        
        # 调整对话框区域边距
        dialog_padx = max(int(self.base_dialog_padx * scale), 20)
        dialog_pady = max(int(self.base_dialog_pady * scale), 10)
        self.dialog_frame.pack_configure(padx=dialog_padx, pady=(0, dialog_pady))
        
        # 调整选项区域边距
        choice_pady_first = max(int(self.base_choice_pady[0] * scale), 10)
        choice_pady_second = max(int(self.base_choice_pady[1] * scale), 10)
        # 只在选项框已经显示时更新边距
        if self.choice_frame.winfo_manager():
            self.choice_frame.pack_configure(pady=(choice_pady_first, choice_pady_second))
        
        # 调整对话文本标签边距
        dialog_label_pady_bottom = max(int(self.base_dialog_label_pady[1] * scale), 2)
        self.dialog_label.pack_configure(pady=(0, dialog_label_pady_bottom))
        
        # 调整内容区域边距
        content_pad_x = max(int(15 * scale), 5)
        content_pad_y = max(int(15 * scale), 5)
        self.dialog_content.pack_configure(padx=content_pad_x, pady=content_pad_y)
        
        # 调整选择按钮边距和内边距
        button_pady = max(int(5 * scale), 2)
        button_ipadx = max(int(self.base_button_ipadx * scale), 10)
        button_ipady = max(int(self.base_button_ipady * scale), 2)
        
        for button in self.choice_buttons:
            button.pack_configure(pady=button_pady, ipadx=button_ipadx, ipady=button_ipady)
            
    def on_show(self):
        """当界面显示时调用"""
        self.is_typing = True
        self.text_finished = False
        self.dialog_label.typewriter_effect(self.dialog_text, delay=50, callback=self.on_text_finished)
        
    def on_text_finished(self):
        """当文本显示完成时调用"""
        self.is_typing = False
        self.text_finished = True
        
    def show_choices(self):
        self.choice_frame.pack(pady=(20, 20))
        
    def on_choice(self, index):
        self.choice_frame.pack_forget()
        self.controller.show_frame("EndScreenFrame")