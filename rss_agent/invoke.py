import deepagents
from deepagents.backends import FilesystemBackend

from rss_agent.subagents import subagents
from rss_agent.tools import tools

SYSTEM_PROMPT = """
You're a RSS feed assistance agent, you do not have any prior knowledge on any of these topics, 
you will answer questions asked by user related to the topics posted in rss feed by fetching from 
vector store db.
"""

backend = FilesystemBackend(root_dir="./",virtual_mode=False)

agent = deepagents.create_deep_agent(
    subagents=subagents,
    tools=tools,
    model="claude-haiku-4.5",
    backend=backend,
    system_prompt=SYSTEM_PROMPT

)
def invoke_agent(query: str):

    user_message = [{"role":"user","content":query}]

    stream = agent.stream_events(input=user_message,version="v3")
    for message in stream.messages:
        for delta in message.reasoning:
            print(f"[thinking] {delta}",end=" ",flush=True)

        for delta in message.text:
            print(f"[thinking] {delta}",end=" ",flush=True)

        for delta in message.tool_calls:
            print(f"[tool call] {delta}",end=" ",flush=True)




