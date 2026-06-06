import asyncio #导入 Python 标准库 asyncio。
#asyncio.sleep()  异步等待
#asyncio.gather() 并发运行多个协程
#asyncio.run() 启动事件循环，运行入口协程

'''
async def task(name:str): #定义协程函数 task
    print(f'{name}开始')
    await asyncio.sleep(2) #表示异步等待 2 秒。
    print(f"{name}结束")

async def main(): #定义入口协程 main
    await asyncio.gather( #同时运行这三个协程，并等待它们全部完成。
        task("任务1"),#调用协程函数后，得到的是三个协程对象。asyncio.gather(...) 把它们一起交给事件循环调度。
        task("任务2"),
        task("任务3"),
    )

asyncio.run(main())#这是程序真正启动的地方。
#1. 创建事件循环
#2. 把 main() 这个协程放进事件循环
#3. 运行 main()
#4. 等 main() 执行完
#5. 关闭事件循环

'''

'''
async def search_tool(query:str)->str:
    print(f"搜索工具开始：{query}")
    await asyncio.sleep(2)
    print(f"搜索工具结束")
    return f"搜索结果：{query}"

async def calculator_tool(expression:str)->str:
    print(f"计算工具开始：{expression}")
    await asyncio.sleep(1)
    print(f'计算工具结束')
    return f"计算结果：{expression} = 42"

async def file_tool(file_name:str):
    print(f"文件工具开始：{file_name}")
    await asyncio.sleep(3)
    print("文件工具结束")
    return f"文件内容：{file_name}"

async def main():
    results =await asyncio.gather(
        search_tool("Python asyncio"),
        calculator_tool("6 * 7"),
        file_tool("notes.md"),
    )
    print("全部工具完成")
    print(results)

asyncio.run(main())

'''
import time
def sync_search_tool(query: str) -> str:
    print(f"同步搜索开始：{query}")
    time.sleep(2)
    print("同步搜索结束")
    return f"搜索结果：{query}"

def sync_calculator_tool(expression: str) -> str:
    print(f"同步计算开始：{expression}")
    time.sleep(1)
    print("同步计算结束")
    return f"计算结果：{expression} = 42"

def sync_file_tool(file_name: str) -> str:
    print(f"同步文件读取开始：{file_name}")
    time.sleep(3)
    print("同步文件读取结束")
    return f"文件内容：{file_name}"

def run_sync_tools() -> list[str]:
    start_time = time.time()

    results = [
        sync_search_tool("Python asyncio"),
        sync_calculator_tool("6 * 7"),
        sync_file_tool("notes.md"),
    ]

    end_time = time.time()
    print(f"同步总耗时：{end_time - start_time:.2f} 秒")
    return results

async def async_search_tool(query: str) -> str:
    print(f"异步搜索开始：{query}")
    await asyncio.sleep(2)
    print("异步搜索结束")
    return f"搜索结果：{query}"


async def async_calculator_tool(expression: str) -> str:
    print(f"异步计算开始：{expression}")
    await asyncio.sleep(1)
    print("异步计算结束")
    return f"计算结果：{expression} = 42"


async def async_file_tool(file_name: str) -> str:
    print(f"异步文件读取开始：{file_name}")
    await asyncio.sleep(3)
    print("异步文件读取结束")
    return f"文件内容：{file_name}"


async def run_async_tools() -> list[str]:
    start_time = time.time()

    results = await asyncio.gather(
        async_search_tool("Python asyncio"),
        async_calculator_tool("6 * 7"),
        async_file_tool("notes.md"),
    )

    end_time = time.time()
    print(f"异步总耗时：{end_time - start_time:.2f} 秒")

    return results


async def main() -> None:
    print("===== 同步工具调用 =====")
    sync_results = run_sync_tools()
    print(sync_results)

    print("\n===== 异步工具调用 =====")
    async_results = await run_async_tools()
    print(async_results)

asyncio.run(main())
