import agents
friday_openai = agents.friday_openai()

def message_openai_agent(messages):
    # Get the last message where the role is "user"
    user_message = [m for m in messages if m["role"] == "user"][-1]["message"]
    print("User Question: " + user_message)

    return friday_openai(user_message)
    
friday_flan= agents.friday_flan()
def message_flan_agent(messages):
    # Get the last message where the role is "user"
    user_message = [m for m in messages if m["role"] == "user"][-1]["message"]
    print("User Question: " + user_message)

    return friday_flan.run(user_message)

friday_alpaca = agents.friday_alpaca()
def message_alpaca_agent(messages):
    # Get the last message where the role is "user"
    user_message = [m for m in messages if m["role"] == "user"][-1]["message"]
    print("User Question: " + user_message)

    return friday_alpaca.run(user_message)