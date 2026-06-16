# 2026-06-06 Asyncio Practice

这个目录是 Python `asyncio` 异步编程练习，用来理解协程、事件循环和并发执行。

练习重点是对比：

```text
同步工具顺序执行
异步工具并发执行
```

这为后续 Agent 多工具调用、FastAPI 异步接口和并发任务处理打基础。

## 学习目标

- 理解 `async def` 定义协程函数
- 理解 `await` 等待异步任务
- 使用 `asyncio.sleep()` 模拟异步 I/O
- 使用 `asyncio.gather()` 并发运行多个协程
- 使用 `asyncio.run()` 启动事件循环
- 对比同步执行和异步并发执行的耗时差异

## 项目结构

```text
2026-06-06-asyncio-practice/
├── asyncio_demo.py
└── README.md
```

## 核心文件

### `asyncio_demo.py`

这个文件包含三部分练习。

第一部分是最小协程示例：

```python
async def task(name: str):
    await asyncio.sleep(2)
```

用于理解：

```text
协程函数
异步等待
事件循环
```

第二部分模拟多个异步工具：

- `search_tool`
- `calculator_tool`
- `file_tool`

通过 `asyncio.gather()` 同时运行多个工具。

第三部分对比同步工具和异步工具：

同步版本：

```text
sync_search_tool
sync_calculator_tool
sync_file_tool
```

异步版本：

```text
async_search_tool
async_calculator_tool
async_file_tool
```

同步工具使用：

```python
time.sleep()
```

异步工具使用：

```python
await asyncio.sleep()
```

## 运行方式

在本目录执行：

```bash
../.venv/bin/python asyncio_demo.py
```

运行后可以观察：

```text
同步总耗时
异步总耗时
```

同步执行会按顺序等待每个工具完成。

异步执行会让多个工具同时等待，因此总耗时更接近最慢的那个任务。

## 关键理解

同步调用：

```text
任务 1 完成
-> 任务 2 开始
-> 任务 3 开始
```

异步并发：

```text
任务 1、任务 2、任务 3 同时开始
-> 谁先完成谁先返回
-> gather 等全部完成
```

`asyncio.gather()` 的作用：

```text
同时运行多个协程，并等待它们全部完成
```

`asyncio.run()` 的作用：

```text
创建事件循环
运行入口协程
协程结束后关闭事件循环
```

## 和后续学习的关系

`asyncio` 后续会帮助理解：

- FastAPI 的 `async def` 路由
- Agent 同时调用多个工具
- 并发搜索、文件读取、网络请求
- 后台任务和异步任务调度
- LLM / RAG 应用里的多步骤异步流程

## 一句话总结

这个练习通过同步和异步工具调用对比，理解 `asyncio` 如何让多个等待型任务并发执行，从而减少总耗时。
