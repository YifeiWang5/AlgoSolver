# ------ LangSmith Set-Up ------
import os
import keyring
SERVICE = "langsmith"
USERNAME = "api_key"
os.environ["LANGSMITH_API_KEY"] = keyring.get_password(SERVICE, USERNAME)
os.environ["LANGSMITH_PROJECT"] = "algo_solver"
os.environ["LANGSMITH_TRACING"] = "true"


import agents.workflow_compiler
from agents.workflow_compiler import app, create_agent_state
from utilities.util_funcs import save_run


# ---- Interactive Session ----
if __name__ == "__main__":

    # Initialize an empty state
    state = create_agent_state() #context=f''

    # Initial full pipeline run
    state = app.invoke(state) 

    # Save graph diagram to folder
    save_run(state, app, run_name='dev_run1', save_path='outputs')

    print('\n\n\n\n======== RESULTS ========\n\n')

    print(f'Code Solution: {state['pseudocode']}\n')

    print(f'Proof of Correctness: {state['proof']}\n')

    print(f'Big-O Notation: {state['complexity']}\n')

    print(f'Real Python Solution: {state['real_code']}\n')