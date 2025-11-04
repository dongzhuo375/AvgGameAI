import tkinter as tk
from tkinter import ttk
import threading
import time

class BaseUI(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # 设置主题
        self.style = ttk.Style()
        self.style.theme_use('clam')  # 使用clam主题

        self.configure_styles()

        self.configure(bg='black')

        self.geometry("1280x720")
        self.minsize(800, 450)  # 设置最小窗口大小
        self.resizable(True, True)
        
        # 绑定窗口关闭事件
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # 初始化基础尺寸
        self.base_width = 1280
        self.base_height = 720
        
        # 绑定窗口大小变化事件
        self.bind("<Configure>", self.on_window_resize)
        self.resize_after_id = None
        
    def configure_styles(self):
        # 配置按钮样式
        self.style.configure(
            'Game.TButton',
            foreground='white',
            background='black',
            font=('微软雅黑', 12),
            borderwidth=2
        )
        self.style.map(
            'Game.TButton',
            foreground=[('active', 'black')],
            background=[('active', 'white')]
        )
        
        # 配置标签样式
        self.style.configure(
            'Title.TLabel',
            foreground='white',
            background='black',
            font=('微软雅黑', 24, 'bold')
        )
        
        self.style.configure(
            'Dialog.TLabel',
            foreground='white',
            background='black',
            font=('微软雅黑', 12),
            wraplength=600
        )
        
        self.style.configure(
            'Choice.TButton',
            foreground='white',
            background='black',
            font=('微软雅黑', 11),
            borderwidth=1
        )
        self.style.map(
            'Choice.TButton',
            foreground=[('active', 'black')],
            background=[('active', 'white')]
        )
        
    def on_window_resize(self, event):
        """处理窗口大小变化事件"""
        # 只处理主窗口的大小变化
        if event.widget == self:
            # 使用防抖技术，避免频繁调整
            if self.resize_after_id:
                self.after_cancel(self.resize_after_id)
            self.resize_after_id = self.after(100, self.apply_resize, event.width, event.height)
            
    def apply_resize(self, width, height):
        """应用窗口大小变化"""
        # 计算缩放比例
        width_ratio = width / self.base_width
        height_ratio = height / self.base_height
        scale = min(width_ratio, height_ratio)  # 使用较小的缩放比例保持宽高比
        
        # 更新样式
        self.update_styles(scale)
        
    def update_styles(self, scale):
        """根据缩放比例更新样式"""
        # 更新标题标签样式
        title_font_size = max(int(24 * scale), 12)
        self.style.configure(
            'Title.TLabel',
            font=('微软雅黑', title_font_size, 'bold')
        )
        
        # 更新对话框标签样式
        dialog_font_size = max(int(12 * scale), 8)
        dialog_wrap_length = max(int(600 * scale), 300)
        self.style.configure(
            'Dialog.TLabel',
            font=('微软雅黑', dialog_font_size),
            wraplength=dialog_wrap_length
        )
        
        # 更新按钮样式
        button_font_size = max(int(12 * scale), 8)
        self.style.configure(
            'Game.TButton',
            font=('微软雅黑', button_font_size)
        )
        
        choice_font_size = max(int(11 * scale), 7)
        self.style.configure(
            'Choice.TButton',
            font=('微软雅黑', choice_font_size)
        )
        
    def on_closing(self):
        """处理窗口关闭事件"""
        self.destroy()

class BaseFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='black')
        self.parent = parent
        self.controller = controller
        self.base_width = 1280
        self.base_height = 720
        
        # 绑定配置变化事件
        self.bind("<Configure>", self.on_frame_configure)
        self.resize_after_id = None
        
    def on_frame_configure(self, event):
        """处理帧配置变化"""
        if event.widget == self:
            # 使用防抖技术
            if self.resize_after_id:
                self.after_cancel(self.resize_after_id)
            self.resize_after_id = self.after(100, self.apply_frame_resize, event.width, event.height)
            
    def apply_frame_resize(self, width, height):
        pass  # 子类可以重写此方法

class RoundedBorderFrame(tk.Frame):
    """
    圆角边框Frame
    """
    def __init__(self, parent, border_width=2, border_color='white', radius=20, padding=10, bg='black', **kwargs):
        # 创建不使用额外容器的Frame
        super().__init__(parent, bg=bg, **kwargs)
        
        # 保存参数
        self.border_width = border_width
        self.border_color = border_color
        self.radius = radius
        self.padding = padding
        self.bg = bg
        self.parent = parent
        
        # 创建Canvas用于绘制圆角边框
        self.canvas = tk.Canvas(
            self,
            bg=bg,
            highlightthickness=0
        )
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # 绑定大小变化事件
        self.bind("<Configure>", self._on_configure)
        
    def _on_configure(self, event=None):
        """处理大小变化"""
        self._draw_border()
        
    def _draw_border(self):
        """绘制圆角边框"""
        # 清除之前的绘制
        self.canvas.delete("border")
        
        # 获取尺寸
        width = self.winfo_width()
        height = self.winfo_height()
        
        if width > 0 and height > 0:
            # 绘制圆角矩形
            self._create_rounded_rect(
                self.canvas,
                self.padding,  # x1
                self.padding,  # y1
                width - self.padding,  # x2
                height - self.padding,  # y2
                self.radius,
                outline=self.border_color,
                width=self.border_width
            )
            
    def _create_rounded_rect(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
        """绘制圆角矩形"""
        points = [
            x1 + radius, y1,
            x1 + radius, y1,
            x2 - radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1 + radius,
            x1, y1,
        ]
        return canvas.create_polygon(points, smooth=True, tags="border", **kwargs)

class TypewriterLabel(ttk.Label):
    """
    实打字机效果标签
    """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.text = ""
        self.displayed_text = ""
        self.index = 0
        self.after_id = None
        self.base_font = None
        self.base_font_size = 12
        self.callback = None
        
        # 获取初始字体信息
        try:
            font = self.cget("font")
            if isinstance(font, str):
                # 如果是字体名称，使用默认大小
                self.base_font = font
            else:
                # 如果是字体元组 (family, size) 或 (family, size, style)
                self.base_font = font[0]
                self.base_font_size = font[1] if len(font) > 1 else 12
        except:
            self.base_font = "微软雅黑"
            self.base_font_size = 12
        
    def typewriter_effect(self, text, delay=50, callback=None):
        """
        打字机效果实现
        
        Args:
            text: 显示的文本
            delay: 字符之间的延迟（毫秒）
            callback: 完成后调用的回调函数
        """
        self.text = text
        self.displayed_text = ""
        self.index = 0
        self.callback = callback
        self._update_text(delay)
        
    def _update_text(self, delay):
        if self.index < len(self.text):
            self.displayed_text += self.text[self.index]
            self.config(text=self.displayed_text)
            self.index += 1
            self.after_id = self.after(delay, self._update_text, delay)
        else:
            if self.callback:
                self.callback()
                
    def skip_typewriter(self):
        """
        立即显示完整文本
        """
        if self.after_id:
            self.after_cancel(self.after_id)
        self.displayed_text = self.text
        self.config(text=self.text)
        if self.callback:
            # 保存回调引用并在调用后清空，防止重复调用
            callback = self.callback
            self.callback = None
            callback()
            
    def update_font_size(self, scale):
        """根据缩放比例更新字体大小"""
        new_font_size = max(int(self.base_font_size * scale), 8)
        self.config(font=(self.base_font, new_font_size))