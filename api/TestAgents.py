import agents

agent = agents.friday_openai()
agent_res = agent.run("What is the meaning of life?")
print(agent_res)