# RAG Knowledge QA System

这是一个基于 FastAPI 的 RAG 知识库问答系统，用于演示文档上传、文本切分、向量检索、基于资料生成回答、引用来源追踪和流式回答的完整后端流程。

项目目标不是只写一个脚本 demo，而是整理成一个具备后端项目结构、接口文档、测试和评测记录的 RAG API 项目。

## 项目亮点

- 支持文档上传和文本切分
- 支持 embedding 向量化
- 使用 Qdrant 保存和检索向量
- 支持 top-k 相似度检索
- 支持基于检索结果生成回答
- 支持 answer + sources 响应结构
- 支持 RAG 流式回答
- 加入 grounding 约束，减少模型幻觉
- 资料不足时主动拒答
- 加入统一异常处理和请求日志
- 补充基础接口测试和 RAG 评测记录

## 技术栈

- Python 3.10
- FastAPI
- Pydantic
- OpenAI-compatible API
- Embedding Model
- Qdrant
- pytest
- python-dotenv

## 项目架构

```text
用户
  |
  v
FastAPI 接口层
  |
  |-- POST /documents/upload
  |      |
  |      v
  |   文档切分 text_splitter
  |      |
  |      v
  |   Embedding 向量化
  |      |
  |      v
  |   Qdrant 向量库入库
  |
  |-- POST /documents/search
  |      |
  |      v
  |   Query 向量化
  |      |
  |      v
  |   Top-k 相似度检索
  |      |
  |      v
  |   返回相关 chunks 和 metadata
  |
  |-- POST /documents/answer
  |      |
  |      v
  |   检索相关 chunks
  |      |
  |      v
  |   拼接 RAG context
  |      |
  |      v
  |   调用 LLM 生成回答
  |      |
  |      v
  |   返回 answer + sources
  |
  |-- POST /documents/answer/stream
         |
         v
      检索相关 chunks
         |
         v
      拼接 RAG context
         |
         v
      调用 LLM stream=True
         |
         v
      流式返回回答，最后追加 sources
```

## 项目结构

```text
2026-07-10-rag-knowledge-qa-system/
├── app/
│   ├── __init__.py
│   ├── exceptions.py
│   ├── logging_config.py
│   ├── main.py
│   ├── rag_service.py
│   ├── schemas.py
│   ├── text_splitter.py
│   └── vector_store.py
├── tests/
│   └── test_api.py
├── .env.example
├── README.md
└── rag_eval.md
```

## 核心模块

`app/main.py`

FastAPI 应用入口，负责接口注册、请求日志和统一异常处理。

`app/schemas.py`

定义 API 请求体和响应体，包括文档上传、检索结果、问答结果和引用来源。

`app/text_splitter.py`

负责将上传文本切分成 chunks，并通过 chunk size 和 overlap 控制切分粒度。

`app/vector_store.py`

负责 embedding 生成、Qdrant collection 初始化、chunks 入库和 top-k 向量检索。

`app/rag_service.py`

负责 RAG 问答流程，包括检索相关 chunks、过滤低相关结果、构造 context、调用 LLM 生成普通回答或流式回答。

`app/exceptions.py`

定义统一业务异常 `RAGServiceError`。

`app/logging_config.py`

配置项目日志格式。

`tests/test_api.py`

提供基础接口测试，覆盖健康检查、请求参数校验和统一异常响应。

`rag_eval.md`

记录 RAG 评测表，用于观察回答准确性、引用质量和失败原因。

## 环境变量

项目使用 `.env` 保存本地真实配置，`.env` 不提交到 GitHub。

`.env.example` 示例：

```env
AIHUBMIX_API_KEY=your-api-key-here
AIHUBMIX_BASE_URL=https://aihubmix.com/v1
AIHUBMIX_MODEL=deepseek-v4-flash
AIHUBMIX_EMBEDDING_MODEL=your-embedding-model
```

## 启动项目

进入项目目录：

```bash
cd /Users/xiongzehao/代码/python进阶/2026-06-study/2026-07-10-rag-knowledge-qa-system
```

启动服务：

```bash
../.venv/bin/python -m uvicorn app.main:app --reload --port 8003
```

访问 Swagger：

```text
http://127.0.0.1:8003/docs
```

健康检查：

```text
GET /health
```

响应示例：

```json
{
  "status": "ok"
}
```

## 核心接口

### 上传文档

```text
POST /documents/upload
```

请求示例：

```json
{
  "filename": "fastapi_auth.md",
  "content": "FastAPI 可以结合 JWT 实现用户登录和接口鉴权。用户登录成功后，后端生成 token，客户端后续请求时在 Authorization header 中携带 token。"
}
```

响应示例：

```json
{
  "filename": "fastapi_auth.md",
  "chunk_count": 1
}
```

### 检索文档

```text
POST /documents/search
```

请求示例：

```json
{
  "query": "FastAPI 登录后客户端怎么携带 token？",
  "top_k": 3
}
```

响应示例：

```json
{
  "query": "FastAPI 登录后客户端怎么携带 token？",
  "results": [
    {
      "chunk_id": "fastapi_auth.md-1-xxxx",
      "text": "用户登录成功后，后端生成 token，客户端后续请求时在 Authorization header 中携带 token。",
      "source": "fastapi_auth.md",
      "paragraph": 1,
      "score": 0.89
    }
  ]
}
```

### 基于资料回答问题

```text
POST /documents/answer
```

请求示例：

```json
{
  "question": "FastAPI 登录后客户端应该怎么携带 token？",
  "top_k": 3
}
```

响应示例：

```json
{
  "question": "FastAPI 登录后客户端应该怎么携带 token？",
  "answer": "根据资料，客户端后续请求时在 Authorization header 中携带 token。",
  "sources": [
    {
      "chunk_id": "fastapi_auth.md-1-xxxx",
      "source": "fastapi_auth.md",
      "paragraph": 1,
      "score": 0.89,
      "text": "用户登录成功后，后端生成 token，客户端后续请求时在 Authorization header 中携带 token。"
    }
  ]
}
```

### 流式回答

```text
POST /documents/answer/stream
```

请求示例：

```json
{
  "question": "RAG 流式输出有什么价值？",
  "top_k": 3
}
```

终端测试：

```bash
curl -N -X POST "http://127.0.0.1:8003/documents/answer/stream" \
  -H "Content-Type: application/json" \
  -d '{"question": "RAG 流式输出有什么价值？", "top_k": 3}'
```

流式接口会先返回模型生成内容，最后追加资料来源。

### 资料不足时的回答

请求示例：

```json
{
  "question": "Django 的 ORM 怎么使用？",
  "top_k": 3
}
```

响应示例：

```json
{
  "question": "Django 的 ORM 怎么使用？",
  "answer": "我没有在已上传的资料中找到相关内容。",
  "sources": []
}
```

## Demo 数据

建议上传以下三段文档，用于项目演示。

### fastapi_auth.md

```text
FastAPI 可以结合 JWT 实现用户登录和接口鉴权。用户登录成功后，后端生成 token，客户端后续请求时在 Authorization header 中携带 token。
```

### rag_streaming.md

```text
RAG 系统会先检索相关 chunks，再把检索结果拼接成 context 交给大模型生成回答。流式输出可以让模型边生成边返回内容，适合长答案和实时交互场景。
```

### docker_deploy.md

```text
Docker 可以把 FastAPI 应用和运行环境打包成容器。Docker Compose 可以同时启动 FastAPI 服务和数据库服务，方便在不同机器上复现运行环境。
```

## Demo 问题

有资料问题：

- FastAPI 登录后客户端应该怎么携带 token？
- RAG 流式输出有什么价值？
- Docker Compose 对后端项目有什么帮助？
- RAG 系统为什么要先检索 chunks？

无资料问题：

- Django 的 ORM 怎么使用？
- Redis 如何实现分布式锁？
- React 组件怎么写？
- Kubernetes 怎么部署服务？

## 期望行为

对于有资料问题，系统应该：

- 检索到相关 chunk
- 基于 sources 中的内容回答
- 不扩展资料中没有的信息
- 返回 answer 和 sources

对于无资料问题，系统应该：

- 不使用模型自己的背景知识强行回答
- 返回“我没有在已上传的资料中找到相关内容。”
- sources 返回空列表

## RAG 关键设计

### Sources

RAG 项目不能只返回 answer，还要返回 sources。

sources 可以说明：

- 回答是根据哪些资料生成的
- 检索到了哪些 chunk
- 回答是否真的有依据
- 后续能否排查回答错误

一个可信的 RAG 回答应该满足：

- answer 中的关键信息能在 sources.text 中找到
- sources.source 来自正确文件
- sources.score 足够高
- 资料不足时不强行回答

### Grounding

Grounding 指的是让模型的回答严格基于给定资料，而不是依赖模型自己的通用知识自由发挥。

本项目通过 prompt 约束模型：

- 只能使用资料中明确出现的信息
- 不能使用背景知识补充答案
- 不能推测、扩展或编造资料外的信息
- 资料不足时必须拒答

### Relevance Threshold

项目会根据相似度阈值过滤低相关 chunks。

阈值过高可能导致有用资料被过滤，系统误判为“没有资料”。阈值过低可能引入无关资料，增加回答噪声。

当前项目将阈值设置为适合演示的范围，用于平衡召回和准确性。

### Streaming

普通 RAG 是等待完整答案生成后一次性返回 answer + sources。

流式 RAG 是在完成检索和 context 构造后，调用 LLM 时开启 `stream=True`，让模型边生成边返回内容。

流式输出主要提升用户体验，尤其适合长答案、实时问答和 Agent 产品展示。它不直接提升回答准确率，准确率仍然依赖 chunk、embedding、top_k、相似度阈值、grounding prompt 和评测。

## 测试

运行测试：

```bash
../.venv/bin/python -m pytest
```

当前测试覆盖：

- `/health` 正常返回
- `/documents/upload` 参数校验
- `/documents/search` 参数校验
- `/documents/answer` 参数校验
- `RAGServiceError` 能返回统一 503 响应

## 评测

项目使用 `rag_eval.md` 记录 RAG 评测结果。

评测重点：

- 回答是否准确
- 回答是否基于资料
- sources 是否真的支持 answer
- 资料不足时是否拒答
- 失败原因是检索问题、生成问题还是引用问题

## 项目讲解顺序

面试或展示时可以按以下顺序讲：

1. 项目解决什么问题：让用户基于已上传资料进行知识库问答。
2. 用户如何上传文档：通过 `/documents/upload` 上传文本。
3. 文档如何处理：切分成 chunks，并写入向量库。
4. 用户提问时怎么检索：query 转向量，执行 top-k 相似度检索。
5. 怎么生成回答：将检索结果拼成 context，要求 LLM 只基于资料回答。
6. 为什么返回 sources：用于验证回答依据和排查错误。
7. 为什么支持 streaming：提升长答案和实时问答体验。
8. 如何评测效果：固定测试问题，记录准确性、引用质量和失败原因。

## 当前不足

- Qdrant 使用本地内存模式，服务重启后数据会丢失
- 只支持手动上传文本，不支持真实文件上传
- 暂不支持 PDF / Markdown 自动解析
- chunk 切分策略仍较简单
- 没有用户系统和文档权限隔离
- 没有前端页面
- RAG 评测还不是自动化流程

## 后续优化方向

- 使用持久化 Qdrant
- 支持真实文件上传
- 支持 PDF / Markdown 解析
- 优化 chunk size 和 overlap
- 加入 rerank
- 加入引用编号
- 加入用户系统和文档权限隔离
- 加入自动化 RAG 评测
- 加入前端页面
