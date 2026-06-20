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


## 模型参数实验

本项目测试了 `temperature`、`top_p`、`max_tokens` 对输出的影响。

测试问题：

```text
请用三句话介绍 FastAPI 的优点。
```

实验结果总结：

| 参数组合 | 观察结果 |
|---|---|
| `temperature=0.1, top_p=1.0, max_tokens=120` | 输出稳定、正式，接近标准答案 |
| `temperature=0.7, top_p=1.0, max_tokens=120` | 输出更自然，内容更丰富 |
| `temperature=1.2, top_p=1.0, max_tokens=120` | 理论上更发散，但简单问题下变化不明显 |
| `temperature=0.7, top_p=0.5, max_tokens=120` | 输出更收敛，扩展内容更少 |
| `temperature=0.7, top_p=1.0, max_tokens=40` | 输出被截断，说明 max_tokens 太小 |

参数理解：

```text
temperature
控制随机性。越低越稳定，越高越开放。

top_p
控制候选词范围。越低越收敛，越高越开放。

max_tokens
控制最大输出长度。太小会导致回答被截断。
```

实际建议：

```text
技术问答：temperature=0.2~0.5
结构化输出：temperature=0.0~0.3
RAG 问答：temperature=0.1~0.3
Agent 工具调用：temperature=0.0~0.3
普通聊天：temperature=0.7 左右
```

## FastAPI Chat API

本项目在最小聊天脚本基础上，新增了 FastAPI 接口。

新增项目结构：

```text
app/
├── __init__.py
├── main.py
├── schemas.py
└── services.py
```

各文件作用：

```text
app/main.py
创建 FastAPI 应用，定义 /health 和 /chat 接口

app/schemas.py
定义 ChatRequest 和 ChatResponse

app/services.py
封装 LLM API 调用逻辑
```

### /chat 接口

请求方式：

```http
POST /chat
```

请求体：

```json
{
  "question": "请用一句话解释 FastAPI。"
}
```

响应体：

```json
{
  "answer": "FastAPI 是一个基于 Python 的现代、高性能 Web 框架..."
}
```

### 启动服务

先加载环境变量：

```bash
export $(cat .env | xargs)
```

启动 FastAPI：

```bash
../.venv/bin/python -m uvicorn app.main:app --reload --port 8001
```

访问 Swagger：

```text
http://127.0.0.1:8001/docs
```

### curl 测试

成功请求：

```bash
curl -X POST "http://127.0.0.1:8001/chat" \
  -H "Content-Type: application/json" \
  -d '{"question": "请用一句话解释 JWT。"}'
```

成功响应：

```json
{
  "answer": "JWT（JSON Web Token）是一种基于JSON的开放标准..."
}
```

失败请求：

```bash
curl -X POST "http://127.0.0.1:8001/chat" \
  -H "Content-Type: application/json" \
  -d '{"question": ""}'
```

失败原因：

```text
question 最小长度是 1，不能为空
FastAPI 自动返回 422
```

### 本次接口链路

```text
客户端请求 /chat
-> FastAPI 接收请求
-> ChatRequest 校验 question
-> ChatService 调用 LLM API
-> ChatResponse 返回 answer
```