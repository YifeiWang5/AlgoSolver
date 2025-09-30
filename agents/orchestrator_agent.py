from init_llm import llm
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
        # if route == "greeting":
        #     state["previous_agent"] = route
        #     state["routing"] = "parsing"

        # elif route == "parsing":
        #     state["previous_agent"] = route
        #     state["routing"] = "strategy"

        if route == "strategy":
            state["previous_agent"] = route
            state["routing"] = "coder"

        elif route == "coder":
            state["previous_agent"] = route
            state["routing"] = "verifier"

        elif route == "prover":
            state["previous_agent"] = route
            state["routing"] = "verifier"

        elif route == "complexity":
            state["previous_agent"] = route
            state["routing"] = "verifier"
            
        elif route == "verifier":
            if state["previous_agent"] == "coder":
                if state["verified"]:
                    state["routing"] = "prover"
                else:
                    state["routing"] = "coder" #loop back if failed check

            if state["previous_agent"] == "prover":
                if state["verified"]:
                    state["routing"] = "complexity"
                else:
                    state["routing"] = "prover" #loop back if failed check

            if state["previous_agent"] == "complexity":
                if state["verified"]:
                    # state["routing"] = "end"
                    state["routing"] = "real_coder"
                else:
                    state["routing"] = "complexity" #loop back if failed check


        elif route == "real_coder":
            state["routing"] = "end"
            # state["previous_agent"] = route
            # state["routing"] = "verifier"

        else:
            state["routing"] = "end"
            # response = llm.invoke(system_prompt)
            # state["routing"] = response.content
    except:
        state["routing"] = "end"
    
    return state