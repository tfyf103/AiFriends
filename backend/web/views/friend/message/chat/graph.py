"""聊天 Agent 的 LangGraph 定义。

本文件只负责“AI 大脑”：LLM、Tool 与图路由。运行模式、模型名和功能开关
统一由 ``web.ai.config`` 管理；RAG 的向量检索细节则下沉到
``web.documents.retrieval``，便于 Chapter 19 单独评测 retrieval。
"""

import os
from typing import Annotated, Sequence, TypedDict

from django.utils.timezone import localtime, now
from langchain_core.messages import BaseMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.constants import END, START
from langgraph.graph import StateGraph, add_messages
from langgraph.prebuilt import ToolNode

from web.ai.config import get_ai_settings
from web.documents.retrieval import format_documents_for_tool, search_documents


class CharGraph:
    """负责创建“聊天角色 Agent”的 LangGraph。"""

    @staticmethod
    def create_app():
        config = get_ai_settings()

        @tool
        def get_time() -> str:
            """当需要查询精确时间时调用。返回本地时间。"""
            return localtime(now()).strftime('%Y-%m-%d %H:%M:%S')

        @tool
        def search_knowledge_base(query: str) -> str:
            """当问题需要查询当前项目私有知识库时调用，返回带来源的相关资料。"""
            documents = search_documents(query, k=3)
            evidence = format_documents_for_tool(documents)
            return f'从知识库中找到以下相关信息：\n\n{evidence}\n'

        # text 模式默认只有不依赖外部向量库的时间工具；full 或显式开启 RAG 才注册检索工具。
        tools = [get_time]
        if config.enable_rag:
            tools.append(search_knowledge_base)

        llm = ChatOpenAI(
            model=config.chat_model,
            openai_api_key=os.getenv('API_KEY'),
            openai_api_base=os.getenv('API_BASE'),
            streaming=True,
            model_kwargs={
                'stream_options': {
                    'include_usage': True,
                },
            },
        ).bind_tools(tools)

        class AgentState(TypedDict):
            messages: Annotated[Sequence[BaseMessage], add_messages]

        def model_call(state: AgentState) -> AgentState:
            res = llm.invoke(state['messages'])
            return {'messages': [res]}

        def should_continue(state: AgentState) -> str:
            last_message = state['messages'][-1]
            if last_message.tool_calls:
                return 'tools'
            return 'end'

        graph = StateGraph(AgentState)
        graph.add_node('agent', model_call)
        graph.add_node('tools', ToolNode(tools))
        graph.add_edge(START, 'agent')
        graph.add_conditional_edges(
            'agent',
            should_continue,
            {
                'tools': 'tools',
                'end': END,
            },
        )
        graph.add_edge('tools', 'agent')
        return graph.compile()
