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
from langchain_core.runnables.config import RunnableConfig

save_path = '2_Add_Two_Numbers'

algo_question = """
You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0 itself.



Example 1:

Input: l1 = [2,4,3], l2 = [5,6,4]
Output: [7,0,8]
Explanation: 342 + 465 = 807.

Example 2:

Input: l1 = [0], l2 = [0]
Output: [0]

Example 3:

Input: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
Output: [8,9,9,9,0,0,0,1]

 


Constraints:

    The number of nodes in each linked list is in the range [1, 100].
    0 <= Node.val <= 9
    It is guaranteed that the list represents a number that does not have leading zeros.



"""

code_struct = '''
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: Optional[ListNode]
        :type l2: Optional[ListNode]
        :rtype: Optional[ListNode]
        """
'''
# ---- Interactive Session ----
if __name__ == "__main__":

    # Initialize an empty state
    state = create_agent_state(context=algo_question, real_code_struct=code_struct, skip_proof=True) #context=f''

    # Initial full pipeline run
    config = RunnableConfig(recursion_limit=50) #max number of graph nodes to process
    state = app.invoke(state, config) 

    # Save graph diagram to folder
    save_run(state, app, run_name=save_path, save_path='outputs')

    print('\n\n\n\n======== RESULTS ========\n\n')

    print(f'Research Findings: {state['research_findings']}\n')

    print(f'Research Summary: {state['research_summary']}\n')

    print(f'Code Solution: {state['pseudocode']}\n')

    print(f'Proof of Correctness: {state['proof']}\n')

    print(f'Big-O Notation: {state['complexity']}\n')

    print(f'Real Python Solution: {state['real_code']}\n')