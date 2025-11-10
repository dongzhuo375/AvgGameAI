import os.path
import tkinter as tk
from tkinter import ttk
import re
from typing import List, Dict, Any
import threading
import time
from playsound import playsound

from audio.audio_player import play_audio
from config.decorators import get_config_dir
from .base_ui import BaseFrame, TypewriterLabel, RoundedBorderFrame

class GameScreenFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        # 游戏状态
        self.current_segments = []       # 存储解析后的段落（包括文本和属性）
        self.current_segment_index = 0   # 当前显示的段落索引
        self.current_choices = []        # 当前选项
        self.is_typing = False
        self.text_finished = False       # 标记文本是否已完成显示
        self.is_waiting_response = False # 标记是否正在等待API响应
        self.chat_session = None         # ChatSession实例
        self.pending_end_text = None     # 待处理的结束文本
        
        self.init_ui()
        
    def init_ui(self):
        """初始化UI组件"""
        # 创建主框架
        self.main_frame = tk.Frame(self, bg='black')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.main_frame.bind("<Button-1>", self.on_click)
        
        # 空白区域
        self.top_spacer = tk.Frame(self.main_frame, bg='black', height=100)
        self.top_spacer.pack(fill=tk.X)
        
        # 选项区域
        self.choice_frame = tk.Frame(self.main_frame, bg='black')
        self.choice_buttons = []
        # 初始化选项按钮
        for i in range(3):  # 最多3个选项
            button = ttk.Button(
                self.choice_frame,
                text="",
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
        
    def reset_game(self):
        """重置游戏状态，用于重新开始游戏"""
        # 清空段落
        self.current_segments = []
        self.current_segment_index = 0
        self.current_choices = []
        self.is_typing = False
        self.text_finished = False
        self.is_waiting_response = False
        self.pending_end_text = None  # 清除待处理的结束文本
        
        # 清空显示文本
        self.dialog_label.config(text="")
        
        # 隐藏选项按钮
        self.choice_frame.pack_forget()
        
        # 重置按钮文本
        for button in self.choice_buttons:
            button.config(text="")
            
    def set_chat_session(self, chat_session):
        """设置ChatSession实例"""
        self.chat_session = chat_session
        
    def start_new_game(self):
        """开始新游戏"""
        self.reset_game()
        if self.chat_session:
            # 显示等待文本
            self.dialog_label.config(text="AI生成中...")
            self.is_waiting_response = True
            
            # 在后台线程中获取初始AI响应
            threading.Thread(target=self._get_initial_response, daemon=True).start()
        
    def _get_initial_response(self):
        """在后台线程中获取初始响应"""
        if self.chat_session:
            response = self.chat_session.get_response()
            # 在主线程中更新UI
            self.after(0, self._handle_response, response)
            
    def _handle_response(self, response):
        """在主线程中处理响应"""
        self.is_waiting_response = False
        if response:
            self.set_ai_response(response)
        
    def parse_ai_response(self, response_text: str) -> Dict[str, Any]:
        """
        解析AI返回的文本，提取[text]、[sound]、[choice]等标签内容
        """
        print(response_text)

        result = {
            "segments": [],  # 统一存储所有段落（包括文本、属性和声音）
            "choices": [],
            "end": None
        }

        lines = response_text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:  # 跳过空行
                continue
                
            if line.startswith('[text]'):
                text_content = line[6:].strip()  # 去掉[text]前缀
                if text_content:
                    result["segments"].append({
                        "type": "text",
                        "content": text_content
                    })
                    
            elif line.startswith('[sound]'):
                sound_content = line[7:].strip()  # 去掉[sound]前缀
                if sound_content:
                    result["segments"].append({
                        "type": "sound",
                        "content": sound_content
                    })
                    # 声音内容不需要在文本框显示，但需要在对应位置触发处理
                    
            elif line.startswith('[attribute='):
                # 解析属性变化，格式: [attribute=属性名.数值]原因+属性变化情况
                match = re.match(r'\[attribute=([^.]+)\.([+-]?\d+)\](.*)', line)
                if match:
                    attr_name, attr_value, reason = match.groups()
                    result["segments"].append({
                        "type": "attribute",
                        "content": reason.strip(),
                        "attribute": {
                            "name": attr_name,
                            "value": int(attr_value),
                            "reason": reason.strip()
                        }
                    })
                    
            elif line.startswith('[choice]'):
                choice_content = line[8:].strip()  # 去掉[choice]前缀
                result["choices"] = [choice.strip() for choice in choice_content.split('|') if choice.strip()]
                
            elif line.startswith('[end]'):
                end_content = line[5:].strip()  # 去掉[end]前缀
                result["end"] = end_content

        return result
        
    def display_next_segment(self):
        """
        显示下一个段落
        """
        if self.current_segment_index < len(self.current_segments):
            # 获取当前段落
            segment = self.current_segments[self.current_segment_index]
            
            if segment["type"] == "text":
                # 显示文本段落
                self.is_typing = True
                self.text_finished = False
                self.dialog_label.typewriter_effect(
                    segment["content"], 
                    delay=50, 
                    callback=self.on_text_finished
                )
            elif segment["type"] == "attribute":
                # 显示属性变更段落
                self.is_typing = True
                self.text_finished = False
                self.dialog_label.typewriter_effect(
                    segment["content"], 
                    delay=50, 
                    callback=lambda: self.on_attribute_segment_finished(segment)
                )
            elif segment["type"] == "sound":
                # 处理声音段落
                self.on_sound_segment_finished(segment)
                # 声音段落不需要显示文本，直接处理下一个段落
                self.current_segment_index += 1
                self.display_next_segment()
                return
            
            self.current_segment_index += 1
        else:
            # 所有段落显示完毕，显示选项
            self.show_choices()
            
    def send_user_choice(self, choice_text: str):
        """发送用户选择并获取响应"""
        if self.chat_session:
            # 隐藏选项按钮
            self.choice_frame.pack_forget()
            
            # 显示等待文本
            self.dialog_label.config(text="AI生成中...")
            self.is_waiting_response = True
            
            # 在后台线程中发送用户选择并获取响应
            threading.Thread(target=self._send_choice_and_get_response, args=(choice_text,), daemon=True).start()
            
    def _send_choice_and_get_response(self, choice_text):
        """在其他线程中发送选择并获取响应"""
        if self.chat_session:
            self.chat_session.add_user_message(choice_text)
            response = self.chat_session.get_response()

            # 在主线程中更新UI
            self.after(0, self._handle_response, response)
            
    def set_ai_response(self, response_text: str):
        """
        设置并处理AI返回的响应文本
        """
        # 解析响应文本
        parsed_data = self.parse_ai_response(response_text)
        
        # 存储段落
        self.current_segments = parsed_data["segments"]
        self.current_choices = parsed_data["choices"]
        self.current_segment_index = 0
        
        # 如果有结束内容，标记需要跳转到结束界面
        self.pending_end_text = parsed_data["end"]
        
        # 更新选项按钮文本
        for i, button in enumerate(self.choice_buttons):
            if i < len(self.current_choices):
                button.config(text=self.current_choices[i])
                button.pack()  # 确保按钮可见
            else:
                button.pack_forget()  # 隐藏多余的按钮
        
        # 隐藏选项框，直到文本显示完毕
        self.choice_frame.pack_forget()
        
        # 开始显示第一个段落
        self.display_next_segment()
        
    def on_click(self, event):
        """处理鼠标点击事件"""
        # 如果正在等待API响应，则不处理点击事件
        if self.is_waiting_response:
            return
            
        if self.is_typing:
            # 如果正在打字效果，跳过
            self.dialog_label.skip_typewriter()
            self.is_typing = False
            self.text_finished = True
            # 不再自动调用display_next_segment，等待下一次点击
        elif self.text_finished:
            # 如果文本已经显示完毕，显示下一段或选项
            if self.current_segment_index < len(self.current_segments):
                self.display_next_segment()
            else:
                # 检查是否有待处理的结束文本
                if hasattr(self, 'pending_end_text') and self.pending_end_text is not None:
                    self.controller.show_frame("EndScreenFrame", end_text=self.pending_end_text)
                    self.pending_end_text = None  # 清除待处理的结束文本
                else:
                    self.show_choices()
        
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
        # 这里可以初始化游戏内容
        pass
        
    def on_text_finished(self):
        """当文本显示完成时调用"""
        self.is_typing = False
        self.text_finished = True
        
    def on_attribute_segment_finished(self, segment):
        """
        当属性段落显示完成时调用
        """
        # 在这里处理属性变更的实时执行
        # 留空等待后续处理
        pass
        
        # 继续处理
        self.is_typing = False
        self.text_finished = True
        # 不再自动调用display_next_segment，等待用户点击

    def on_sound_segment_finished(self, segment):
        """
        当声音段落处理完成时调用
        """
        # 从段落内容中获取声音文件名并播放
        sound_file = segment["content"]
        sound_path = os.path.join(get_config_dir(), "data", f"sounds/{sound_file}.mp3")
        try:
            playsound(sound_path)
        except Exception as e:
            print(f"播放声音失败: {e}")
        
    def show_choices(self):
        """
        显示选项按钮
        """
        if self.current_choices:
            self.choice_frame.pack(pady=(70, 10))
        
    def on_choice(self, index):
        """
        处理选项选择
        """
        if index < len(self.current_choices):
            # 发送用户选择到AI并获取响应
            print(self.current_choices[index])
            self.send_user_choice(self.current_choices[index])