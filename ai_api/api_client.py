import time

from openai import OpenAI

from config.decorators import config_value


@config_value("api_key", ".....")
def get_key(api_key):
    print(f"API Key = {api_key}")
    return api_key

@config_value("base_url", ".....")
def get_url(base_url):
    print(f"Base URL = {base_url}")
    return base_url

@config_value("timeout", 30)
def get_timeout(timeout):
    print(f"timeout = {timeout}")
    return timeout

@config_value("model", "deepseek/deepseek-v3.1-terminus")
def get_model(model):
    print(f"Model = {model}")
    return model

class ChatSession:
    def __init__(self):
        self.messages = []
        self.client = OpenAI(
            api_key= get_key(),
            base_url= get_url(),
            timeout= get_timeout(),  # 全局超时设置
        )
        self.model = get_model()

    def add_user_message(self, content):
        self.messages.append({"role": "user", "content": content})

    def get_response(self):
        print("正在请求AI接口，请耐心等待...")
        start_time = time.time()
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                timeout=150.0  # 设置超时时间
            )
            ai_content = response.choices[0].message.content
            self.messages.append({"role": "assistant", "content": ai_content})
            end_time = time.time()
            print(f"请求完成，耗时：{end_time - start_time:.2f}秒")
            return ai_content
        except Exception as e:
            print(f"请求发生错误: {e}")
            return None
