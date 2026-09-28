import deepagents
from deepagents.backends import FilesystemBackend
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace

from rss_agent.subagents import subagents
from rss_agent.tools import tools

SYSTEM_PROMPT = """
You're a RSS feed assistance agent, you do not have any prior knowledge on any of these topics, 
you will answer questions asked by user related to the topics posted in rss feed by fetching from 
vector store db.
"""

backend = FilesystemBackend(root_dir="./",virtual_mode=False)

llm_endpoint = HuggingFaceEndpoint(
    model="Qwen/Qwen3.8-27B",
    task="text-generation",
    temperature=0.1,
)
llm = ChatHuggingFace(llm=llm_endpoint)

agent = deepagents.create_deep_agent(
    subagents=subagents,
    tools=tools,
    model=llm,
    backend=backend,
    system_prompt=SYSTEM_PROMPT

)
def invoke_agent(query: str):

    user_message = [{"role":"user","content":query}]

    stream = agent.stream_events(input=user_message,version="v3")
    for message in stream.messages:
        for delta in message.reasoning:
            yield {"thinking":delta}

        for delta in message.text:
            yield {"text":delta}
        for delta in message.tool_calls:
            yield {"tool":delta}


if __name__ == "__main__":
    query = input("Enter query: ")
    print(invoke_agent(query))

