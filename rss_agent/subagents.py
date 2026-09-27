from deepagents import SubAgent

subagents: list[SubAgent] = []

def get_subagent(agent: SubAgent):
    return subagents

def add_subagent(agent: SubAgent):
    subagents.append(agent)
    return agent
