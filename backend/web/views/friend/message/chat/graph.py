"""
聊天 Agent 的 LangGraph 定义。

如果把 chat.py 理解成“总调度器”，那么这个文件就是“AI 大脑的执行流程图”。

当前图结构：

    START
      |
      v
    agent  ----没有 tool_calls----> END
      |
      | 有 tool_calls
      v
    tools
      |
      +---------------------------> agent

含义：
1. 先让 LLM 看消息；
2. 如果 LLM 认为需要工具，就进入 ToolNode；
3. 工具执行结果会加入 messages；
4. 再回到 LLM，让它基于工具结果组织最终答案；
5. 没有更多工具调用时结束。

这正是一个最小但完整的“Agent + Function Calling + RAG”示例。
"""

import os
from typing import TypedDict, Annotated, Sequence

import lancedb
from django.utils.timezone import localtime, now
from langchain_community.vectorstores import LanceDB
from langchain_core.messages import BaseMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.constants import START, END
from langgraph.graph import add_messages, StateGraph
from langgraph.prebuilt import ToolNode

from web.documents.utils.custom_embeddings import CustomEmbeddings


class CharGraph:
    """负责创建“聊天角色 Agent”的 LangGraph。"""

    @staticmethod
    def create_app():
        """
        创建并 compile 一张新的 LangGraph。

        返回的 app 可以：
        - app.invoke(...)：一次性执行；
        - app.stream(...)：同步流式执行；
        - app.astream(...)：异步流式执行。

        chat.py 中为了同时做 TTS，使用的是 app.astream(...)。
        """

        # ------------------------------------------------------------------
        # Tool 1：查询当前时间
        # ------------------------------------------------------------------
        @tool
        def get_time() -> str:
            """
            当需要查询精确时间时，调用此函数。返回格式为：[年-月-日 时:分:秒]

            @tool 会把普通 Python 函数转换成 LangChain Tool。
            函数名、类型标注和 docstring 都会帮助 LLM 理解：
            “这个工具叫什么、什么时候应该使用、会返回什么”。
            """
            return localtime(now()).strftime('%Y-%m-%d %H:%M:%S')

        # ------------------------------------------------------------------
        # Tool 2：RAG 知识库检索
        # ------------------------------------------------------------------
        @tool
        def search_knowledge_base(query: str) -> str:
            """
            当用户查询阿里云百炼平台的相关信息时，调用此函数。
            输入为要查询的问题，输出为知识库中最相关的文本片段。

            这就是项目当前的 RAG“检索”阶段：

                用户问题
                  -> Embedding
                  -> LanceDB 相似度搜索
                  -> Top 3 文本片段
                  -> 返回给 LLM
                  -> LLM 根据资料生成答案

            注意：这个函数本身不负责“生成答案”，它只负责“查资料”。
            最终回答仍由 agent 节点中的 LLM 完成。
            """
            # LanceDB 是本地向量数据库。
            db = lancedb.connect('./web/documents/lancedb_storage')

            # 查询文本必须使用与建库阶段一致/兼容的 Embedding 模型转换成向量。
            embeddings = CustomEmbeddings()

            # 将已有 LanceDB table 包装成 LangChain VectorStore，方便调用 similarity_search。
            vector_db = LanceDB(
                connection=db,
                embedding=embeddings,
                table_name='my_knowledge_base',
            )

            # k=3 表示只拿最相关的 3 个文本块，避免把整份文档塞给模型。
            docs = vector_db.similarity_search(query, k=3)

            # 将 Document 对象整理成普通字符串，作为 ToolMessage 的结果返回给 Agent。
            context = '\n\n'.join([
                f'内容片段：{i + 1}\n{doc.page_content}'
                for i, doc in enumerate(docs)
            ])

            return f'从知识库中找到以下相关信息：\n\n{context}\n'

        # 所有允许 LLM 调用的工具集中放在这里。
        tools = [get_time, search_knowledge_base]

        # ------------------------------------------------------------------
        # LLM
        # ------------------------------------------------------------------
        llm = ChatOpenAI(
            # 项目当前通过 OpenAI-compatible API 调用该模型。
            model="deepseek-v4-pro",
            openai_api_key=os.getenv('API_KEY'),
            openai_api_base=os.getenv('API_BASE'),

            # 开启 streaming 后，chat.py 才能逐块拿到模型输出。
            streaming=True,

            # 要求兼容服务在流式结果中附带 token 使用量。
            model_kwargs={
                "stream_options": {
                    "include_usage": True,
                }
            }

        # bind_tools 的核心意义：把工具的 schema 告诉模型。
        # 模型并不会直接执行 Python 函数，它只会输出“我想调用哪个工具 + 参数”。
        # 真正执行函数的是下面的 ToolNode。
        ).bind_tools(tools)

        # ------------------------------------------------------------------
        # State：图在节点之间传递的数据
        # ------------------------------------------------------------------
        class AgentState(TypedDict):
            # Sequence[BaseMessage]：状态里保存一串 System/Human/AI/Tool Message。
            # Annotated[..., add_messages]：新节点返回消息时，不覆盖旧列表，而是追加/合并。
            messages: Annotated[Sequence[BaseMessage], add_messages]

        # ------------------------------------------------------------------
        # Node 1：agent
        # ------------------------------------------------------------------
        def model_call(state: AgentState) -> AgentState:
            """把当前所有 messages 交给 LLM，并把 LLM 的新消息写回状态。"""
            res = llm.invoke(state['messages'])
            return {'messages': [res]}

        # ------------------------------------------------------------------
        # Router：决定 agent 之后去 tools 还是 END
        # ------------------------------------------------------------------
        def should_continue(state: AgentState) -> str:
            """
            LLM 如果返回 tool_calls，说明它暂时不想直接回答，而是想先查工具。
            否则说明已经得到最终自然语言答案，可以结束。
            """
            last_message = state['messages'][-1]

            if last_message.tool_calls:
                return "tools"

            return "end"

        # ToolNode 会读取 AIMessage.tool_calls，找到对应 Python Tool，
        # 执行后把结果作为 ToolMessage 追加回 messages。
        tool_node = ToolNode(tools)

        # ------------------------------------------------------------------
        # Build Graph
        # ------------------------------------------------------------------
        graph = StateGraph(AgentState)

        # 注册节点：名字可以自定义，但后面连边时必须一致。
        graph.add_node('agent', model_call)
        graph.add_node('tools', tool_node)

        # 第一步永远进入 agent。
        graph.add_edge(START, 'agent')

        # agent 执行完后不是固定去某处，而是调用 should_continue 动态判断。
        graph.add_conditional_edges(
            'agent',
            should_continue,
            {
                'tools': 'tools',
                'end': END,
            }
        )

        # 工具执行完后必须回到 agent：
        # 因为 Tool 返回的是“原始资料”，还需要 LLM 把资料组织成人类可读答案。
        graph.add_edge('tools', 'agent')

        # compile() 将“图的定义”变成真正可以 invoke/stream/astream 的应用。
        return graph.compile()
