def user_interface_agent(state):
    prompt_for_user = """
I am an expert algorithm solver!\n
In the solution I will provide peusdocode, proof of correctness, and time complexity.\n\n
Please input the algorithm problem below (paste as single line):\n
"""
    init_user_input = input(prompt_for_user)

    provided_code_struct = input("\n\nCopy and paste (paste as single line) the desired code output structure (i.e. leetcode answer template). Otherwise reply 'NO'.\n\n")
    state["real_code_struct"] = provided_code_struct

    user_input = init_user_input + '\n' + provided_code_struct

    # if len(provided_code_struct) > 10: #not sure
    #     state["real_code_struct"] = provided_code_struct
    
    if state["context"] is None:
        state["context"] = init_user_input
    else:
        state["context"] = state["context"] + f'\nUser: {init_user_input}\n'
    
    # state["routing"] = "Parsing"
    state["messages"] = [
        {"role":"assistant", "content": prompt_for_user},
        {"role":"user", "content": user_input}
    ]

    return state