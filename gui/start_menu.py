import tkinter as tk
from tkinter import ttk
from .base_ui import BaseFrame, RoundedBorderFrame

class StartMenuFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        # 居中显示主框架
        self.main_frame = tk.Frame(self, bg='black')
        self.main_frame.pack(expand=True)

        self.title_label = ttk.Label(
            self.main_frame, 
            text="AVG 游戏", 
            style='Title.TLabel'
        )
        self.title_label.pack(pady=(30, 30))

        self.choices = ["开始游戏", "游戏设置", "退出游戏"]
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
            height=6,
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
        
        # 确认按钮
        self.confirm_button = ttk.Button(
            self.main_frame,
            text="确认",
            style='Game.TButton',
            command=self.on_confirm
        )
        self.confirm_button.pack(pady=(0, 30))

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
            
            if choice == "开始游戏":
                self.controller.show_frame("GameScreenFrame")
            elif choice == "游戏设置":
                # 这里可以添加设置界面
                pass
            elif choice == "退出游戏":
                self.controller.on_closing()