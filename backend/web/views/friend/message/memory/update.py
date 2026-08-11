"""
长期记忆更新逻辑。

AiFriends 当前没有把“所有聊天历史”永久塞进每一次 LLM 请求，而是采用两层记忆：

1. 短期记忆：最近 10 条 Message 原文；
2. 长期记忆：Friend.memory 中的一段压缩摘要。

chat.py 每累计 5 条聊天记录会调用 update_memory(friend)。
这个文件会把“旧长期记忆 + 最近 10 条聊天”交给一个专门的 MemoryGraph，
让 LLM 重新整理出一份新的长期记忆。

可以把它理解为：

旧摘要 + 新发生的事情 -> 记忆整理模型 -> 新摘要

这是一种非常适合教学的长期记忆方案，因为实现简单，而且能直观看到“上下文压缩”的思想。
"""

from django.utils.timezone import now
from langchain_core.messages import SystemMessage, HumanMessage

from web.models.friend import SystemPrompt, Message
from web.views.friend.message.memory.graph import MemoryGraph


def create_system_message():
    """
    构造“记忆整理任务”的系统提示词。

    Django Admin 中 title='记忆' 的 SystemPrompt 会按 order_number 排序后拼接。
    因此记忆提炼规则可以放在数据库中修改，而不必每次改 Python 源码。

    例如可以告诉模型：
    - 保留用户稳定的偏好；
    - 保留重要人物关系；
    - 忽略寒暄和短期无关细节；
    - 不要凭空编造没有出现过的信息。
    """
    system_prompts = SystemPrompt.objects.filter(title='记忆').order_by('order_number')

    prompt = ''
    for sp in system_prompts:
        prompt += sp.prompt

    return SystemMessage(prompt)


def create_human_message(friend):
    """
    把“旧长期记忆”和“最近聊天原文”打包成一条 HumanMessage。

    为什么不是只给最近聊天？
    因为旧摘要里可能保存着更早但仍然重要的信息。
    如果每次只总结最近 10 条，早期信息会在多轮更新后逐渐消失。
    """
    prompt = f'[原始记忆]\n{friend.memory}\n'
    prompt += '[最近对话]\n'

    # 先拿最新 10 条，再 reverse()，保证交给模型的顺序是从旧到新。
    messages = list(Message.objects.filter(friend=friend).order_by('-id')[:10])
    messages.reverse()

    for m in messages:
        prompt += f'user: {m.user_message}\n'
        prompt += f'ai: {m.output}\n'

    return HumanMessage(prompt)


def update_memory(friend):
    """
    真正执行一次长期记忆压缩，并写回 Friend.memory。

    这里使用同步 invoke()，因为记忆更新不需要实时展示给前端用户。
    与聊天主回复不同，它是一个后台式的“整理动作”。
    """
    app = MemoryGraph.create_app()

    inputs = {
        'messages': [
            create_system_message(),
            create_human_message(friend),
        ]
    }

    # MemoryGraph 只有一个 LLM 节点，所以最终 messages[-1] 就是新的 AI 摘要。
    res = app.invoke(inputs)
    friend.memory = res['messages'][-1].content

    # 同时更新时间，方便以后观察某个好友的记忆最后一次何时被整理。
    friend.update_time = now()
    friend.save()
