from init_llm import llm

def prover_agent(state):

    system_prompt = f"""
# Role
You are an expert at proving that a Pseudocode Solution is correct for an Algorithm Problem. 

# Task
Given an Algorithm Problem and Pseudocode Solution, provide a formal proof of correctness. **If** you cannot create a valid proof, reply with "Proof not available."

# Algorithm Problem: {state["problem_spec"]}

# Pseudocode Solution: {state['pseudocode']}


# Output: **ONLY** the formal proof of correctness. **If** you cannot create a valid proof, reply with "Proof not available."

"""
    if state["skip_proof"]:
        state["proof"] = "\nPROOF SKIPPED\n"
        state["previous_agent"] = "prover"
        state["routing"] = "verifier"
        state["verified"] = True
        
    else:
        response = llm.invoke(system_prompt)
        state["messages"].append({"role":"prover", "content": f'Proof of Correctness: {response.content}'})
        state["proof"] = response.content
    return state