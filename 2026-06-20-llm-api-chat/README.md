# 2026-06-20 LLM API Chat

这是一个基于 FastAPI 的 LLM Chat API 学习项目，用于练习通过 OpenAI 兼容接口调用大模型，并逐步实现单轮聊天、多轮对话、流式输出、错误处理、日志记录和 token 使用量记录。

本项目使用的是 aihubmix.com 的 OpenAI 兼容接口，模型示例为 `deepseek-v4-flash`。

## 学习目标

- 理解 LLM API 的基本请求结构
- 使用 OpenAI Python SDK 调用兼容接口
- 理解 `system`、`user`、`assistant` 三类消息
- 使用环境变量管理 API Key、Base URL 和模型名
- 编写最小单轮聊天脚本
- 理解 `temperature`、`top_p`、`max_tokens` 参数
- 使用 FastAPI 封装 `/chat` 接口
- 使用 `session_id` 实现简单多轮对话
- 使用内存保存对话历史
- 实现上下文长度裁剪
- 实现普通响应和流式响应
- 给 LLM API 调用加入统一异常处理
- 加入请求日志、错误日志和 token usage 日志
- 实现简单 retry 机制

## 项目结构

```text
2026-06-20-llm-api-chat/
├── .env.example
├── README.md
├── chat.py
├── parameter_experiment.py
└── app/
    ├── __init__.py
    ├── exceptions.py
    ├── logging_config.py
    ├── main.py
    ├── memory.py
    ├── schemas.py
    └── services.py
```

## 文件说明

```text
chat.py
最小 LLM API 调用脚本，用于理解 OpenAI SDK 的基础调用方式。

parameter_experiment.py
模型参数实验脚本，用于测试 temperature、top_p、max_tokens 对输出的影响。

app/main.py
FastAPI 应用入口，定义 /health、/chat、/chat/stream 接口，并注册请求日志和统一异常处理。

app/schemas.py
定义 API 请求和响应模型，例如 ChatRequest、ChatResponse。

app/services.py
封装 LLM API 调用逻辑，包括普通响应、流式响应、retry、错误日志和 token usage 日志。

app/memory.py
使用内存字典保存多轮对话历史，并实现上下文裁剪。

app/exceptions.py
定义项目自定义异常，例如 LLMServiceError。

app/logging_config.py
定义日志基础配置。
```

## 环境变量

本项目使用 `.env` 保存本地真实配置，但 `.env` 不提交到 GitHub。

`.env.example` 示例：

```env
AIHUBMIX_API_KEY=your-api-key-here
AIHUBMIX_BASE_URL=https://aihubmix.com/v1
AIHUBMIX_MODEL=deepseek-v4-flash
```

## 安装依赖

在项目根目录的上一级共享虚拟环境中安装依赖。

```bash
../.venv/bin/python -m pip install openai python-dotenv fastapi uvicorn
```

如果已经安装过，可以跳过。

## 启动服务

进入项目目录：

```bash
cd /Users/xiongzehao/Desktop/python进阶/2026-06-study/2026-06-20-llm-api-chat
```

启动 FastAPI：

```bash
../.venv/bin/python -m uvicorn app.main:app --reload --port 8001
```

访问 Swagger：

```text
http://127.0.0.1:8001/docs
```

## 健康检查接口

请求方式：

```http
GET /health
```

响应示例：

```json
{
  "status": "ok"
}
```

## 普通聊天接口

请求方式：

```http
POST /chat
```

请求体：

```json
{
  "session_id": "demo-session",
  "question": "请用一句话解释 FastAPI。"
}
```

响应体：

```json
{
  "session_id": "demo-session",
  "answer": "FastAPI 是一个基于 Python 的现代、高性能 Web 框架..."
}
```

curl 示例：

```bash
curl -X POST "http://127.0.0.1:8001/chat" \
  -H "Content-Type: application/json" \
  -d '{"session_id": "demo-session", "question": "请用一句话解释 JWT。"}'
```

## 流式聊天接口

请求方式：

```http
POST /chat/stream
```

请求体：

```json
{
  "session_id": "stream-demo",
  "question": "请用三句话解释什么是 FastAPI。"
}
```

curl 测试：

```bash
curl -N -X POST "http://127.0.0.1:8001/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{"session_id": "stream-demo", "question": "请用三句话解释什么是 FastAPI。"}'
```

说明：

```text
/chat 是普通响应，模型生成完成后一次性返回完整 answer。
/chat/stream 是流式响应，模型边生成边返回内容。
```

## 多轮对话

本项目使用 `session_id` 区分不同会话。

同一个 `session_id` 下的连续请求会共享历史上下文。

示例：

第一次请求：

```json
{
  "session_id": "demo-session",
  "question": "请用一句话解释 FastAPI。"
}
```

第二次请求：

```json
{
  "session_id": "demo-session",
  "question": "它和 Flask 有什么区别？"
}
```

如果第二次仍然使用同一个 `session_id`，模型可以理解“它”指的是 FastAPI。

如果换成新的 `session_id`，模型就不会拥有上一轮上下文。

## 上下文裁剪

多轮对话历史保存在内存中。

为了避免上下文无限增长，项目会限制历史消息数量。

```text
只保留最近若干条 user / assistant 消息
过旧的消息会被裁剪
```

这样可以控制 token 消耗，也避免请求越来越慢。

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

## 错误处理

项目中定义了统一异常：

```text
LLMServiceError
```

当 LLM API 调用失败时，服务层会捕获底层 `OpenAIError`，然后抛出 `LLMServiceError`。

FastAPI 在 `app/main.py` 中统一捕获该异常，并返回：

```json
{
  "code": "LLM_SERVICE_ERROR",
  "message": "LLM service is temporarily unavailable"
}
```

状态码：

```text
503 Service Unavailable
```

## retry 机制

普通 `/chat` 接口实现了简单 retry。

```text
最多重试 2 次
每次失败后等待 1 秒
```

总请求次数是：

```text
第 1 次：正常尝试
第 2 次：第 1 次重试
第 3 次：第 2 次重试
```

如果 3 次都失败，就返回统一的 `503` 错误。

注意：

```text
/chat 支持 retry
/chat/stream 暂时不做 retry
```

原因是流式接口可能已经返回了一部分内容，如果中途失败后直接重试，可能导致客户端收到重复内容。

## 日志

项目中包含三类日志：

```text
请求日志
记录 method、path、status_code、duration

错误日志
记录 LLM API 调用失败信息

token usage 日志
记录 prompt_tokens、completion_tokens、total_tokens
```

示例：

```text
INFO app.main POST /chat 200 1.2345s
INFO app.services LLM usage prompt_tokens=20 completion_tokens=50 total_tokens=70
ERROR app.services LLM API error attempt=1 error=...
```

## 常见错误

请求体缺少字段：

```json
{
  "question": "请解释 FastAPI"
}
```

返回：

```text
422 Unprocessable Entity
```

原因：

```text
缺少 session_id
请求没有通过 ChatRequest 校验
```

API Key 错误：

```text
.env 中 AIHUBMIX_API_KEY 配置错误
```

返回：

```json
{
  "code": "LLM_SERVICE_ERROR",
  "message": "LLM service is temporarily unavailable"
}
```

状态码：

```text
503
```

区别：

```text
422 = 请求格式错误，由 Pydantic 校验返回
503 = 请求格式正确，但 LLM 服务调用失败
```

## 当前能力

目前项目已经实现：

- 最小 LLM API 调用脚本
- 模型参数实验
- FastAPI `/chat` 接口
- FastAPI `/chat/stream` 接口
- Pydantic 请求和响应模型
- 基于 `session_id` 的多轮对话
- 内存版对话历史
- 上下文长度裁剪
- 普通响应
- 流式响应
- 统一异常处理
- 请求日志
- 错误日志
- token usage 日志
- 简单 retry

## 当前限制

- 对话历史只保存在内存中，服务重启后会丢失
- 暂时没有接入数据库或 Redis
- 暂时没有用户系统
- 暂时没有权限隔离
- 流式接口暂时没有 retry
- 还没有补充自动化测试

## 下一步

- 补充基础测试
- 将对话历史持久化
- 接入用户身份
- 按用户隔离会话
- 为 RAG 和 Agent 工具调用打基础