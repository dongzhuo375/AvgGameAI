import os
import tkinter as tk
from tkinter import ttk

from config.decorators import get_config_manager
from service.story_service import get_stories, get_stories_path
from .base_ui import BaseFrame, RoundedBorderFrame

class StartMenuFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        # 居中显示主框架
        self.main_frame = tk.Frame(self, bg='black')
        self.main_frame.pack(expand=True)

        self.title_label = ttk.Label(
            self.main_frame, 
            text="选择故事",
            style='Title.TLabel'
        )
        self.title_label.pack(pady=(30, 30))

        self.choices = get_stories()
        self.selected_index = 0
        
        # 边框容器
        self.listbox_frame = RoundedBorderFrame(
            self.main_frame,
            border_width=2,
            border_color='white',
            radius=15,
            padding=5,
            bg='black'
        )
        self.listbox_frame.pack(pady=(0, 20), padx=20, fill='x')
        
        # 边框容器内容框架
        self.listbox_content = tk.Frame(self.listbox_frame, bg='black')
        self.listbox_content.pack(fill='both', expand=True, padx=15, pady=15)

        self.listbox = tk.Listbox(
            self.listbox_content,
            width=30,
            height=14,
            font=('微软雅黑', 14),
            bg='black',
            fg='white',
            selectbackground='white',
            selectforeground='black',
            highlightthickness=0,
            bd=0,
            relief='flat'
        )
        self.listbox.pack(side='left', fill='both', expand=True)
        
        # 滚动条
        scrollbar = tk.Scrollbar(self.listbox_content, orient='vertical', command=self.listbox.yview)
        scrollbar.pack(side='right', fill='y')
        self.listbox.config(yscrollcommand=scrollbar.set)
        
        # 添加选项到listbox
        for choice in self.choices:
            self.listbox.insert(tk.END, choice)
            
        # 默认选中第一个选项
        self.listbox.selection_set(0)
        self.listbox.activate(0)
        
        # 按钮框架
        self.button_frame = tk.Frame(self.main_frame, bg='black')
        self.button_frame.pack(pady=(0, 30))
        
        # 开始
        self.confirm_button = ttk.Button(
            self.button_frame,
            text="开始",
            style='Game.TButton',
            command=self.on_confirm
        )
        self.confirm_button.pack(side='left', padx=(0, 50))
        
        # 退出
        self.exit_button = ttk.Button(
            self.button_frame,
            text="退出",
            style='Game.TButton',
            command=controller.on_closing
        )
        self.exit_button.pack()

        self.bind('<Up>', self.move_selection_up)
        self.bind('<Down>', self.move_selection_down)
        self.bind('<Return>', lambda e: self.on_confirm())
        self.focus_set()

        self.listbox_base_font_size = 14
        
    def apply_frame_resize(self, width, height):
        width_ratio = width / self.base_width
        height_ratio = height / self.base_height
        scale = min(width_ratio, height_ratio)
        
        # 调整列表框字体大小
        listbox_font_size = max(int(self.listbox_base_font_size * scale), 8)
        self.listbox.config(font=('微软雅黑', listbox_font_size))
        
        # 调整内边距
        title_pad_y = max(int(30 * scale), 10)
        self.title_label.pack_configure(pady=(title_pad_y, title_pad_y))
        
        listbox_pad_y = max(int(20 * scale), 5)
        self.listbox_frame.pack_configure(pady=(0, listbox_pad_y))
        
        button_pad_y = max(int(30 * scale), 10)
        self.confirm_button.pack_configure(pady=(0, button_pad_y))
        
        # 调整内容区域边距
        content_pad_x = max(int(15 * scale), 5)
        content_pad_y = max(int(15 * scale), 5)
        self.listbox_content.pack_configure(padx=content_pad_x, pady=content_pad_y)
        
    def move_selection_up(self, event):
        current = self.listbox.curselection()[0] if self.listbox.curselection() else 0
        if current > 0:
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(current - 1)
            self.listbox.activate(current - 1)
            self.listbox.see(current - 1)
            
    def move_selection_down(self, event):
        current = self.listbox.curselection()[0] if self.listbox.curselection() else 0
        if current < self.listbox.size() - 1:
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(current + 1)
            self.listbox.activate(current + 1)
            self.listbox.see(current + 1)
            
    def on_confirm(self):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            choice = self.choices[index]
            story_path = get_stories_path()

            yaml_file = os.path.join(story_path, f"{choice}.yaml")
            yml_file = os.path.join(story_path, f"{choice}.yml")

            # 检测文件类型并执行相应函数
            if os.path.exists(yaml_file):
                print(f"找到 YAML 文件: {yaml_file}")
                get_config_manager().setup_story_config(yaml_file)
            elif os.path.exists(yml_file):
                print(f"找到 YML 文件: {yml_file}")
                get_config_manager().setup_story_config(yml_file)
            else:
                print(f"错误：找不到故事文件 '{choice}'")
                print(f"在目录 {story_path} 中未找到 {choice}.yaml 或 {choice}.yml")
                return False

            self.controller.show_frame("GameScreenFrame")