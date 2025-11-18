# AvgGameAI

Python 作业：AI 驱动的 AVG（叙事冒险）游戏

这是一个用 Python 编写的 AVG（冒险视觉小说）游戏项目框架，包含图形界面、配置管理、音频播放。该仓库是Python课的作业。

主要特性
- 基于 tkinter 的 GUI（StartMenuFrame、GameScreenFrame、EndScreenFrame）
- 配置管理（config.json 与 config/ 下的 YAML）
- 简单的音频播放接口（audio 目录）
- 与 AI 后端的会话封装（ai_api.api_client.ChatSession）
- 测试/演示脚本（test.py）

快速开始

1) 克隆仓库并进入目录
```bash
git clone https://github.com/dongzhuo375/AvgGameAI.git
cd AvgGameAI
```

2) 建议使用虚拟环境并安装依赖
```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

requirements.txt（仓库中列出）
- openai>=2.7.1
- PyYAML>=6.0.2
- playsound>=1.2.2
- requests>=2.32.3
- pydantic>=2.12.3
- typing_extensions>=4.15.0

配置（重要）
- 根目录的 config.json 包含运行时需要的字段，当前占位示例：
```json
{
  "api_key": "你的API KEY",
  "base_url": "基础url",
  "model": "模型名",
  "timeout": 30,
  "sounds": { ... }
}
```
请把 "api_key" / "base_url" / "model" 替换为你的实际服务 / 模型配置（如果使用 OpenAI，请填入有效的 Key 或在 ai_api 中使用环境变量方式）。

- 项目会尝试读取 config/ 下的 YAML（如 `config/story.yaml`、`config/config.yaml`），test.py 中也会检查 `config/config.yaml` 和 `config/story.yaml`。如需故事/场景配置，请在 config 目录添加相应的 YAML 文件。

运行项目（GUI）
- 启动主程序（tkinter GUI）：
```bash
python main.py
```
main.py 中会：
- 初始化 ConfigManager（读取根目录 config.json）
- 设置 stories 路径到 `data/stories`
- 启动 MainApp（包含 StartMenuFrame、GameScreenFrame、EndScreenFrame）
- 在启动新游戏时创建 ai_api.api_client.ChatSession()

运行测试/示例脚本
- test.py 提供了若干调试与测试函数：
  - test_config(): 测试配置加载与装饰器
  - test_audio(): 播放 resources/test.mp3（请确保提供音频资源）
  - test_start_menu(): 启动一个简单的 GUI 测试实例
  - test_story_config()/test_config_loader_yaml(): 对 YAML 配置加载器的测试

运行示例：
```bash
python test.py
```

路径与资源提示
- 音频资源：test.py 中示例路径为 `resources/test.mp3`（请将实际音频文件放在该路径或修改路径）
- 故事文件：`data/stories`（main.py 将 stories 路径设为 repository 根的 data/stories）
- GUI 框架文件位于 gui/ 目录（StartMenuFrame、GameScreenFrame、EndScreenFrame、base_ui）

代码结构（仓库根目录）
- main.py — 应用入口，MainApp（tkinter）初始化与运行
- test.py — 测试/演示脚本，包含多项功能测试
- config.json — 全局配置示例（需替换 API Key 等）
- requirements.txt — 依赖列表
- ai_api/ — AI 后端相关客户端（包含 ChatSession 等）
- audio/ — 音频相关实现（audio_player）
- config/ — YAML 配置（story.yaml、config.yaml 等）
- data/ — 游戏数据存放（stories 等）
- gui/ — 界面实现（各 Frame）
- service/ — 业务逻辑服务（例如 story_service）
- LICENSE — 仓库许可证（请查看以确认使用条款）

注意事项与常见问题
- tkinter：在某些 Linux 发行版上需要额外安装系统包（如 Debian/Ubuntu: `sudo apt install python3-tk`）。
- playsound: 在不同平台上的表现可能不同，测试音频播放时若遇问题可考虑替换为其他音频库（例如 pygame、pydub + simpleaudio）。
- OpenAI / AI 后端：ChatSession 与 ai_api 需要有效的 API 配置（config.json 或环境变量）。请避免将真实密钥直接提交到仓库，优先使用环境变量或 CI secrets。
- YAML 配置：test.py 中使用 YamlConfigLoader，如果没有对应的 YAML 文件，测试会跳过相应检查或报找不到文件的提示。
