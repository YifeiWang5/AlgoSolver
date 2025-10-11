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

save_path = '13_Roman_to_Integer'

algo_question = """
Roman numerals are represented by seven different symbols: I, V, X, L, C, D and M.

Symbol       Value
I             1
V             5
X             10
L             50
C             100
D             500
M             1000

For example, 2 is written as II in Roman numeral, just two ones added together. 12 is written as XII, which is simply X + II. The number 27 is written as XXVII, which is XX + V + II.

Roman numerals are usually written largest to smallest from left to right. However, the numeral for four is not IIII. Instead, the number four is written as IV. Because the one is before the five we subtract it making four. The same principle applies to the number nine, which is written as IX. There are six instances where subtraction is used:

    I can be placed before V (5) and X (10) to make 4 and 9. 
    X can be placed before L (50) and C (100) to make 40 and 90. 
    C can be placed before D (500) and M (1000) to make 400 and 900.

Given a roman numeral, convert it to an integer.

 

Example 1:

Input: s = "III"
Output: 3
Explanation: III = 3.

Example 2:

Input: s = "LVIII"
Output: 58
Explanation: L = 50, V= 5, III = 3.

Example 3:

Input: s = "MCMXCIV"
Output: 1994
Explanation: M = 1000, CM = 900, XC = 90 and IV = 4.

 

Constraints:

    1 <= s.length <= 15
    s contains only the characters ('I', 'V', 'X', 'L', 'C', 'D', 'M').
    It is guaranteed that s is a valid roman numeral in the range [1, 3999].

"""

code_struct = '''
class Solution(object):
    def romanToInt(self, s):
        """
        :type s: str
        :rtype: int
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