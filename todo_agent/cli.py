"""命令行交互入口。

这是项目唯一 import openai 的地方：从环境变量读取 DeepSeek 配置，
创建真实 client，与 TodoStore 一起组装出 TodoAgent，然后进入 REPL 循环。

用法：
    DEEPSEEK_API_KEY=你的key python -m todo_agent.cli
"""

import os

from openai import OpenAI

from .agent import TodoAgent
from .store import TodoStore

DEFAULT_BASE_URL = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-v4-flash"


def main() -> None:
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        print("错误：请先设置 DEEPSEEK_API_KEY 环境变量。")
        print("示例：DEEPSEEK_API_KEY=你的key python -m todo_agent.cli")
        return

    base_url = os.environ.get("DEEPSEEK_BASE_URL", DEFAULT_BASE_URL)
    model = os.environ.get("DEEPSEEK_MODEL", DEFAULT_MODEL)

    client = OpenAI(api_key=api_key, base_url=base_url)
    agent = TodoAgent(TodoStore(), client, model=model)

    print("Todo Agent 已启动（输入 exit / quit / 退出 结束）")
    while True:
        try:
            user_input = input("你 > ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if user_input.strip().lower() in ("exit", "quit", "退出"):
            break

        if not user_input.strip():
            continue

        print(agent.run(user_input))


if __name__ == "__main__":
    main()
