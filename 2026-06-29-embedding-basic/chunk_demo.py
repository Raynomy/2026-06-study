def split_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)

        start = end - overlap

    return chunks


def split_markdown_by_heading(markdown_text: str) -> list[str]:
    chunks = []
    current_chunk = []

    for line in markdown_text.strip().splitlines():
        if line.startswith("#") and current_chunk:
            chunk = "\n".join(current_chunk).strip()
            if chunk:
                chunks.append(chunk)

            current_chunk = []

        current_chunk.append(line)

    if current_chunk:
        chunk = "\n".join(current_chunk).strip()
        if chunk:
            chunks.append(chunk)

    return chunks


plain_text = """
FastAPI 是一个现代 Python Web 框架，适合构建 API。
它支持自动生成文档、请求参数校验、依赖注入和异步处理。
在实际后端项目中，FastAPI 常常会结合 SQLAlchemy、JWT、Docker 和 pytest 使用。
SQLAlchemy 负责数据库操作，JWT 用于用户登录鉴权，Docker 用于容器化部署，pytest 用于自动化测试。
"""

markdown_text = """
# FastAPI 项目说明

FastAPI 是一个现代 Python Web 框架，适合构建 API。

## 鉴权

FastAPI 可以结合 JWT 实现用户登录和接口鉴权。

## 数据库

SQLAlchemy 是 Python 常用的 ORM，可以用来操作数据库。

## 测试

pytest 可以用来给 FastAPI 接口编写自动化测试。

## 部署

Docker 可以把应用和运行环境打包成容器。
"""

configs = [
    {"chunk_size": 30, "overlap": 5},
    {"chunk_size": 50, "overlap": 10},
    {"chunk_size": 100, "overlap": 20},
]

print("=" * 60)
print("按固定字符切分")

for config in configs:
    print("=" * 60)
    print(f"chunk_size={config['chunk_size']}, overlap={config['overlap']}")

    chunks = split_text(
        text=plain_text,
        chunk_size=config["chunk_size"],
        overlap=config["overlap"],
    )

    print(f"chunk 数量：{len(chunks)}")

    for index, chunk in enumerate(chunks, start=1):
        print("-" * 40)
        print(f"Chunk {index}")
        print(chunk)

print("=" * 60)
print("按 Markdown 标题切分")

markdown_chunks = split_markdown_by_heading(markdown_text)

print(f"chunk 数量：{len(markdown_chunks)}")

for index, chunk in enumerate(markdown_chunks, start=1):
    print("-" * 40)
    print(f"Chunk {index}")
    print(chunk)