"""LLM 编排层：把用户输入、LLM、工具三者串起来。

TodoAgent 负责「LLM ↔ 工具」之间的多轮循环：
1. 把 system + user 消息连同工具定义发给 LLM。
2. 若模型返回 tool_calls，则逐个执行工具并把结果回传，进入下一轮。
3. 若模型只返回文本，则该文本即最终回答。

本模块不 import openai，client 由外部注入，因此可用 mock 测试，
也不感知 API Key / base_url 等敏感信息。
"""

import json

from .store import TodoStore
from .tools import TOOLS, execute_tool

SYSTEM_PROMPT = "你是一个待办事项助手。请根据用户的需求，使用提供的工具来管理待办事项。"


class TodoAgent:
    """编排 LLM 与工具之间的多轮调用。"""

    def __init__(
        self,
        store: TodoStore,
        client,
        model: str,
        max_iterations: int = 5,
    ) -> None:
        self.store = store
        self.client = client
        self.model = model
        self.max_iterations = max_iterations

    def run(self, user_message: str) -> str:
        """处理一条用户消息，返回最终回答文本。"""
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ]

        for _ in range(self.max_iterations):
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=TOOLS,
            )
            message = response.choices[0].message

            if not message.tool_calls:
                return message.content

            messages.append(message)
            for tool_call in message.tool_calls:
                name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                result = execute_tool(name, arguments, self.store)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                })

        return "抱歉，处理过程中出现了问题，请重试。"
