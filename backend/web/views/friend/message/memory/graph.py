"""
专门用于“整理长期记忆”的 LangGraph。

它和聊天 CharGraph 的最大区别：

聊天图：
    agent -> 可能调用 tools -> agent -> ... -> END

记忆图：
    START -> agent -> END

原因很简单：记忆更新只需要让 LLM 根据已有内容生成一份新摘要，
不需要查时间、知识库或其他外部工具。

这个文件非常适合初学 LangGraph：先学会一个只有 1 个节点的图，再去看 chat/graph.py 的条件分支和 ToolNode。
"""

import os
from typing import TypedDict, Annotated, Sequence

from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.constants import START, END
from langgraph.graph import add_messages, StateGraph


class MemoryGraph:
    """创建一个最小 LangGraph，用于长期记忆摘要。"""

    @staticmethod
    def create_app():
        # ChatOpenAI 不只可以调用 OpenAI 官方模型。
        # 只要服务提供 OpenAI-compatible API，就可以通过 base_url/API_BASE 接入。
        llm = ChatOpenAI(
            model="deepseek-v4-pro",
            openai_api_key=os.getenv('API_KEY'),
            openai_api_base=os.getenv('API_BASE'),
        )

        class AgentState(TypedDict):
            """
            图的状态定义。

            messages 是 LangGraph 在节点之间传递的核心数据。
            add_messages 表示节点返回的新消息会与旧消息合并，而不是直接覆盖整个列表。
            """
            messages: Annotated[Sequence[BaseMessage], add_messages]

        def model_call(state: AgentState) -> AgentState:
            """
            唯一的业务节点：把记忆整理提示词交给 LLM。

            输入通常是：
            SystemMessage(记忆整理规则)
            HumanMessage(旧记忆 + 最近聊天)

            输出是一条新的 AIMessage，也就是新的长期记忆文本。
            """
            res = llm.invoke(state['messages'])
            return {'messages': [res]}

        # 1. 创建一张状态类型为 AgentState 的图。
        graph = StateGraph(AgentState)

        # 2. 把普通 Python 函数注册成图节点。
        graph.add_node('agent', model_call)

        # 3. 定义固定流程：START -> agent -> END。
        graph.add_edge(START, 'agent')
        graph.add_edge('agent', END)

        # 4. compile 后才得到可以 invoke() 的可执行应用。
        return graph.compile()
