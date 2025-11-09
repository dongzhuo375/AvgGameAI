import time

from openai import OpenAI

from config.decorators import config_value, get_config_manager


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


def sys_text():
    cm = get_config_manager()
    text = f"""现在你是一个ai文字游戏生成工具，通过生成文本内容帮助游戏进行下去。在模仿galgame的语言方式生成具有故事性的长篇文本（至少{cm.get_story_value("text_length.min")}字，即每次生成的故事文本在抛出选项前应该至少200字，可以根据故事节奏延长到至多{cm.get_story_value("text_length.max")}字）后，抛出具有截然不同结果的选项，注意，为了更像gal，需要对文本进行多段分割，长文本按照0~120字以语句连贯性为标准进行分割，分割字数不需要相似以实现更像gal的效果，分割的文本需要在最前端加上[text]以便客户端处理,每次生成文本都要遵守这个原则。

这个故事提供了以下重要角色需要出现在故事中（角色特点要在故事中体现，不应直接在生成的文本中直接说出诸如性格特点等）：
{cm.get_story_value("characters")}

这是一个以{cm.get_story_value("story_type")}为基调的故事，这个故事必须遵守以下原则：
{cm.get_story_value("story_constraints")}

客户端为这个故事提供了以下音效果（键名为音效名）：
{cm.get_global_value("sounds")}
调用音效以类似文本分割的方式进行，但是是以"[sound]音效名"进行

故事中固定以下几个属性以供故事的主角使用，用于判定事件进行的顺利与否以及成败和结局的好坏判定（键名为属性名）：
{cm.get_story_value("attributes")}
增降属性以类似文本分割的方式进行，但是是以"[attribute=属性名.数值]原因"进行(使用例子"[attribute=SAN.5]SAN值增加了5"或"[attribute=SAN.-5]SAN值减少了5")

当一段文本结束需要出现选项时，以"[choice]选项1|选项2|选项3"方式提供三个选项，出现选项时不应继续生成文本而应等待玩家抉择。
当故事完结时，应该提供数百字的较长的故事结束文本，以"[end]结束文本"方式使用。


你需要对故事进行自由把控，灵活使用音效、属性，并且绝对遵守故事原则，充分调动角色。为了便于你理解，接下来为你提供一个视力
----示例开始----
[sound]wyj
[text]一片黑暗
[text]黑暗中，我盲目的跑来跑去，力气，越来越少。
[text]一束亮光没有预兆的出现，照在了我的四周，失去的力气好像回到了自己的身体里。一个纯白色的身影拍打着翅膀慢慢飞下，就像天使一样。
[attribute=力量.5]神奇的光束，略微增强了力量
[text]“天使”在慢慢下降，白色的躯壳出现了一丝丝裂纹。他的外表在崩坏，逐渐露出了腐烂得像尸体一样的真身。
[attribute=SAN.-10]恶心的、恐怖的东西
[sound]heart
[text]醒了。
[text]还好只是一个梦。
[choice]再睡会|去洗把脸|仔细回味梦境
(省略故事)
[text]那个永远让人觉得无所不能的大叔，最终带着笑意躺在了血泊中，再也不能摸我的头了...
[end]大叔死后，我（结束性故事，略，在这里可以交代大叔死后故事的直接状态，以及事件结束一段时间后我的生活状态，以及可以对整个故事作一个总结性的陈述）
----示例结束----

现在我要求以下面的故事背景为故事主题及舞台，开始这场游戏。
故事背景：
{cm.get_story_value("background")}

现在开始这个故事吧。"""
    return text


class ChatSession:
    def __init__(self):
        self.messages = []
        self.client = OpenAI(
            api_key= get_key(),
            base_url= get_url(),
            timeout= get_timeout(),  # 全局超时设置
        )
        self.model = get_model()
        self.messages.append({"role": "system", "content": sys_text()})

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


