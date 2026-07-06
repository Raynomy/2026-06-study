# RAG Document API

这是一个基于 FastAPI 的 RAG 文档问答练习项目。

项目目标是把“文档上传、文本切分、向量检索、基于资料生成回答、返回引用来源”串成一个完整后端 API 流程。

## 一、项目目标

本项目主要练习：

- 使用 FastAPI 设计后端接口
- 将文本切分为 chunks
- 使用 embedding 将文本转换为向量
- 使用 Qdrant 保存和检索向量
- 将检索结果拼接进 prompt
- 调用 LLM 基于资料生成回答
- 返回 answer 和 sources
- 加入 grounding 约束，减少模型幻觉
- 加入统一异常处理、日志和基础测试

## 二、项目结构

```text
2026-07-02-rag-generation-flow/
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

## 三、核心文件职责

`app/main.py`

FastAPI 应用入口，负责注册接口、统一异常处理和请求日志。

`app/schemas.py`

定义 API 请求体和响应体，包括文档上传、检索结果、问答结果和引用来源。

`app/text_splitter.py`

负责将长文本切分成 chunks，并通过 chunk size 和 overlap 控制切分粒度。

`app/vector_store.py`

负责 embedding 生成、Qdrant collection 初始化、chunks 入库和 top-k 向量检索。

`app/rag_service.py`

负责 RAG 生成回答流程：检索相关 chunks，过滤低相关结果，拼接 context，构造 prompt，调用 LLM，并返回 answer + sources。

`app/exceptions.py`

定义统一业务异常 `RAGServiceError`。

`app/logging_config.py`

配置项目日志格式。

`tests/test_api.py`

提供基础接口测试，覆盖健康检查、请求参数校验和统一异常响应。

`rag_eval.md`

记录 RAG 评测表，用于观察回答准确性、引用质量和失败原因。

## 四、环境变量

项目使用 `.env` 保存本地真实配置，`.env` 不提交到 GitHub。

`.env.example` 示例：

```env
AIHUBMIX_API_KEY=your-api-key-here
AIHUBMIX_BASE_URL=https://aihubmix.com/v1
AIHUBMIX_MODEL=deepseek-v4-flash
AIHUBMIX_EMBEDDING_MODEL=your-embedding-model
```

## 五、启动项目

进入项目目录：

```bash
cd /Users/xiongzehao/代码/python进阶/2026-06-study/2026-07-02-rag-generation-flow
```

启动服务：

```bash
.venv/bin/python -m uvicorn app.main:app --reload --port 8003
```

访问 Swagger：

```text
http://127.0.0.1:8003/docs
```

健康检查：

```text
GET /health
```

响应：

```json
{
  "status": "ok"
}
```

## 六、核心接口

### 1. 上传文档

```text
POST /documents/upload
```

作用：

上传一段文本，系统会将文本切分为 chunks，并写入向量库。

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

### 2. 检索文档

```text
POST /documents/search
```

作用：

根据用户 query 检索最相关的 chunks。

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

### 3. 基于资料回答问题

```text
POST /documents/answer
```

作用：

先检索相关 chunks，再将检索结果作为 context 交给 LLM 生成回答。

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

## 七、RAG 完整流程

```text
用户上传文档
-> 文档切分成 chunks
-> chunks 转成 embedding
-> chunks 写入 Qdrant 向量库
-> 用户提出问题
-> 问题转成 embedding
-> 从 Qdrant 检索相关 chunks
-> 根据相似度阈值过滤低相关 chunks
-> 将高相关 chunks 拼接成 context
-> 将 context 和 question 组成 prompt
-> 调用 LLM 生成回答
-> 返回 answer 和 sources
```

## 八、为什么要返回 sources

RAG 项目不能只返回 answer，还要返回 sources。

sources 可以说明：

- 回答是根据哪些资料生成的
- 检索到了哪些 chunk
- 回答是否真的有依据
- 后续能否排查回答错误

这也是 RAG 项目区别于普通聊天机器人的关键点。

一个可信的 RAG 回答应该满足：

- answer 中的关键信息能在 sources.text 中找到
- sources.source 来自正确文件
- sources.score 足够高
- 资料不足时不强行回答

## 九、Grounding 约束

Grounding 指的是让模型的回答严格基于给定资料，而不是依赖模型自己的通用知识自由发挥。

在 RAG 项目中，grounding 的核心是：

```text
先检索资料
再把资料拼成 context
最后要求模型只能根据 context 回答
```

如果没有 grounding 约束，模型可能会：

- 使用自己的背景知识补充答案
- 回答资料中没有出现的内容
- 在资料不足时仍然给出看似合理的回答
- 产生幻觉

例如用户问：

```text
Django 的 ORM 怎么使用？
```

如果资料中没有 Django ORM，系统应该返回：

```text
我没有在已上传的资料中找到相关内容。
```

而不是让模型凭自己的通用知识回答 Django ORM。

## 十、资料不足时的处理

本项目通过两层方式处理资料不足：

- 检索后使用相似度阈值过滤低相关 chunks
- 如果没有相关 chunks，直接返回固定拒答

拒答内容：

```text
我没有在已上传的资料中找到相关内容。
```

这样可以减少幻觉，让系统更可靠。

## 十一、RAG 调参记录

本项目主要观察两个参数：

- `chunk_size`：每个 chunk 的文本长度
- `top_k`：每次检索返回多少个 chunk

### chunk_size

`chunk_size` 太小：

- 容易切断句子
- 语义不完整
- 可能只命中局部关键词

`chunk_size` 太大：

- 上下文更完整
- 但可能混入弱相关内容
- prompt 噪声变多

当前项目使用：

```python
chunk_size = 180
overlap = 40
```

### top_k

`top_k = 1`：

- 上下文更干净
- 不容易带入无关内容
- 但可能漏掉补充信息

`top_k = 3`：

- 召回内容更多
- 更可能补齐上下文
- 但容易带入弱相关 chunks

调参目标不是让返回内容越多越好，而是：

- 召回足够相关的资料
- 减少无关资料进入 prompt
- 让 LLM 基于更干净的 context 回答

## 十二、异常处理和日志

本项目加入了统一业务异常 `RAGServiceError`。

主要覆盖：

- embedding 失败
- 向量库写入失败
- 向量库检索失败
- LLM 生成失败

统一错误响应示例：

```json
{
  "code": "EMBEDDING_ERROR",
  "message": "Failed to create embedding"
}
```

项目也加入了请求日志，方便观察：

- 请求方法
- 请求路径
- 状态码
- 请求耗时

示例：

```text
INFO app.main POST /documents/search 200 0.1234s
```

## 十三、测试

运行测试：

```bash
.venv/bin/python -m pytest
```

当前测试覆盖：

- `/health` 正常返回
- `/documents/upload` 参数校验
- `/documents/search` 参数校验
- `/documents/answer` 参数校验
- `RAGServiceError` 能返回统一 503 响应

测试意义：

保证后续改接口、改异常处理、改 schemas 时，基础行为不会轻易坏掉。

## 十四、RAG 评测

项目中使用 `rag_eval.md` 记录 RAG 评测结果。

评测重点：

- 回答是否准确
- 回答是否基于资料
- sources 是否真的支持 answer
- 资料不足时是否拒答
- 失败原因是检索问题、生成问题，还是引用问题

本阶段观察到：

- 当检索命中正确资料时，回答整体比较稳定
- 主要失败原因来自检索召回不足
- sources 对排查错误非常重要
- RAG 评测不能只看单次回答，需要固定测试问题反复观察

## 十五、当前项目不足

当前项目仍然是学习版 RAG，有几个明显不足：

- Qdrant 使用本地内存模式，服务重启后数据会丢失
- 只支持手动上传文本，不支持真实文件上传
- 暂不支持 PDF / Markdown 自动解析
- chunk 切分策略还比较简单
- 没有用户系统和文档权限隔离
- 没有前端页面
- RAG 评测还不是自动化流程

这些也是后续继续迭代成简历项目的方向。

## 十六、后续优化方向

可以继续扩展：

- 使用持久化 Qdrant
- 支持真实文件上传
- 支持 PDF / Markdown 解析
- 优化 chunk size 和 overlap
- 加入 rerank
- 加入引用编号
- 加入用户系统和文档权限隔离
- 加入自动化 RAG 评测
- 加入前端页面

## 十七、项目复盘

这个项目已经跑通了 RAG 的主链路：

```text
文档上传
-> 文本切分
-> 向量化
-> 向量检索
-> 上下文拼接
-> 基于资料生成回答
-> 返回引用来源
-> 异常处理
-> 日志
-> 测试
```

它已经不是单个脚本 demo，而是一个有后端项目结构的 RAG API 雏形。

从学习角度看，这个项目把 FastAPI 后端能力和 LLM/RAG 能力连接起来了。

从项目展示角度看，它已经具备后续继续打磨成简历项目的基础。
