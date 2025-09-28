
#OpenAI
import os
import keyring
from langchain_openai import ChatOpenAI
os.environ["OPENAI_API_KEY"] = keyring.get_password('openai', 'api_key')
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def orchestrator_agent(state):
#     system_prompt = f"""
# # Role
# You are the workflow orchestrator. 

# # Task
# Based on the current state and the previous agent, determine which agent the workflow should go to next. 

# # Previous Agent: {state["routing"]}


# # Output: **ONLY** a string of the next agent

# """
    route = state["routing"]
    try: #go to next agent step
        if route == "greeting":
            state["previous_agent"] = route
            state["routing"] = "parsing"
        elif route == "parsing":
            state["previous_agent"] = route
            state["routing"] = "strategy"
        elif route == "strategy":
            state["previous_agent"] = route
            state["routing"] = "coder"
        elif route == "coder":
            state["previous_agent"] = route
            state["routing"] = "verifier"
        elif route == "verifier":
            if state["previous_agent"] == "coder":
                if state["verified"]:
                    state["routing"] = "end" #replace with next step (proof agent)
                    # state["routing"] = "prover"
                else:
                    state["routing"] = "coder" #loop back to coder if failed check

        else:
            state["routing"] = "end"
            # response = llm.invoke(system_prompt)
            # state["routing"] = response.content
    except:
        state["routing"] = "end"
    
    return state