# 2026-07-01 RAG Document API

这是一个最小版 RAG 文档检索 API 项目。

项目目标：

- 接收文档文本
- 将文档切分成 chunks
- 调用 embedding model 生成向量
- 将向量和 metadata 写入 Qdrant
- 根据用户 query 检索相关 chunks
- 返回 text、source、paragraph、score

## 项目结构

2026-07-01-rag-document-api/
app/
__init__.py
main.py
schemas.py
text_splitter.py
vector_store.py
.env.example
README.md

## 环境变量

本地需要创建 `.env` 文件。

示例：

AIHUBMIX_API_KEY=your-api-key-here
AIHUBMIX_BASE_URL=https://aihubmix.com/v1
AIHUBMIX_EMBEDDING_MODEL=text-embedding-3-small

## 启动服务

../.venv/bin/python -m uvicorn app.main:app --reload --port 8002

Swagger 地址：

http://127.0.0.1:8002/docs

## 接口说明

### GET /health

健康检查接口。

响应示例：

{
  "status": "ok"
}

### POST /documents/upload

上传文档文本，并写入向量库。

请求示例：

{
  "filename": "fastapi_notes.md",
  "content": "FastAPI 是一个现代 Python Web 框架，适合构建 API。FastAPI 可以结合 JWT 实现用户登录和接口鉴权。"
}

响应示例：

{
  "filename": "fastapi_notes.md",
  "chunk_count": 1
}

### POST /documents/search

根据 query 检索相关文档片段。

请求示例：

{
  "query": "FastAPI 怎么实现登录鉴权？",
  "top_k": 3
}

响应示例：

{
  "query": "FastAPI 怎么实现登录鉴权？",
  "results": [
    {
      "chunk_id": "fastapi_notes.md-1-5f5a3a94",
      "text": "FastAPI 是一个现代 Python Web 框架...",
      "source": "fastapi_notes.md",
      "paragraph": 1,
      "score": 0.8409
    }
  ]
}

## 核心流程

POST /documents/upload
-> split_text()
-> get_embedding()
-> add_chunks()
-> Qdrant upsert

POST /documents/search
-> get_embedding(query)
-> Qdrant query_points
-> 返回 text / source / paragraph / score

## 当前限制

- 当前使用 Qdrant 内存模式，服务重启后数据会丢失
- 目前只支持直接上传文本，不支持真实文件上传
- chunk 策略较简单，只按固定字符长度切分
- 目前只做检索，还没有接入 chat model 生成最终答案