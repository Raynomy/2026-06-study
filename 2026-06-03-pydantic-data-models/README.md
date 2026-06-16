# 2026-06-03 Pydantic Data Models

这个目录是 Pydantic 数据模型练习，用来学习如何用 `BaseModel` 和 `Field` 定义结构化数据，并让 Pydantic 自动完成字段校验。

## 学习目标

- 学习 Pydantic `BaseModel`
- 使用 `Field` 添加字段限制
- 使用 `Literal` 限制固定取值
- 理解数据模型和数据校验
- 为后续 FastAPI 请求体和响应模型打基础

## 项目结构

```text
2026-06-03-pydantic-data-models/
├── app/
│   ├── models.py
│   └── services.py
├── tests/
│   └── test_task_service.py
├── main.py
├── requirements.txt
└── README.md
```

## 核心文件

### `app/models.py`

定义了三个 Pydantic 数据模型：

- `User`
- `Task`
- `Document`

其中包括：

- 字符串最小长度校验
- 字符串最大长度校验
- 年龄范围校验
- 任务状态枚举
- 文档类型枚举

示例：

```python
TaskStatus = Literal["todo", "doing", "done"]
DocumentType = Literal["note", "pdf", "markdown", "web"]
```

### `main.py`

用于手动创建 `User`、`Task`、`Document` 对象，并观察 Pydantic 的校验效果。

当字段不符合模型约束时，会捕获：

```python
ValidationError
```

并输出校验失败信息。

### `app/services.py`

当前是预留文件，后续可用于编写任务或文档相关业务逻辑。

### `tests/test_task_service.py`

当前是预留测试文件，后续可用于测试 service 层逻辑。

## 运行方式

在本目录执行：

```bash
../.venv/bin/python main.py
```

如果使用本目录自己的依赖文件，也可以先安装：

```bash
../.venv/bin/python -m pip install -r requirements.txt
```

## 当前学习重点

这一天的重点不是 Web API，而是先把数据结构定义清楚。

后续 FastAPI 中的：

- 请求体模型
- 响应模型
- 参数校验
- Swagger 文档结构

都会建立在这里学到的 Pydantic 模型基础上。

## 一句话总结

这个练习用 Pydantic 定义 `User`、`Task`、`Document` 三类数据结构，帮助理解“先定义数据模型，再让程序自动校验数据”的后端开发思路。
