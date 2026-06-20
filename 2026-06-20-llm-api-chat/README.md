# 2026-06-20 LLM API Chat

这是 LLM API 学习的第一个项目，用于练习通过 OpenAI 兼容接口调用大模型，并完成最小单轮聊天脚本。

## 学习目标

- 理解 LLM API 的基本请求结构
- 使用 OpenAI Python SDK 调用兼容接口
- 理解 `system`、`user`、`assistant` 三类消息
- 使用环境变量管理 API Key、Base URL 和模型名
- 编写最小单轮聊天脚本

## 项目结构

```text
2026-06-20-llm-api-chat/
├── chat.py
├── .env.example
└── README.md
```

## 环境变量

本项目使用 `.env` 保存本地真实配置，但 `.env` 不提交到 GitHub。

`.env.example` 示例：

```env
AIHUBMIX_API_KEY=your-api-key-here
AIHUBMIX_BASE_URL=https://aihubmix.com/v1
AIHUBMIX_MODEL=deepseek-v4-flash
```

## 核心代码

`chat.py` 中通过 OpenAI SDK 创建客户端：

```python
client = OpenAI(
    api_key=os.getenv("AIHUBMIX_API_KEY"),
    base_url=os.getenv("AIHUBMIX_BASE_URL"),
)
```

通过模型名调用聊天接口：

```python
response = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "system",
            "content": "你是一个简洁清晰的 Python 后端学习助手。",
        },
        {
            "role": "user",
            "content": question,
        },
    ],
)
```

## 三类消息

`system`：

```text
规定模型的角色、语气和行为方式
```

`user`：

```text
用户提出的问题
```

`assistant`：

```text
模型之前回答过的内容，常用于多轮对话上下文
```

## 运行方式

先加载本地环境变量：

```bash
export $(cat .env | xargs)
```

运行脚本：

```bash
../.venv/bin/python chat.py
```

## 测试结果

运行成功后，模型返回了关于 FastAPI 的一句话解释，说明：

```text
API Key 可用
Base URL 可用
模型名称可用
OpenAI SDK 可以调用 aihubmix 兼容接口
最小单轮问答流程跑通
```

## 当前限制

- 目前只支持单轮问答
- 还没有接入 FastAPI API
- 还没有保存多轮对话历史
- 还没有实现流式输出
- 还没有统一错误处理和重试

## 下一步

- 实现多轮对话
- 设计 `/chat` API
- 实现流式输出
- 加入错误处理、日志和 token 使用记录