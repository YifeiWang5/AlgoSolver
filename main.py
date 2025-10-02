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

save_path = '4_Median_of_Two_Sorted_Arrays'

algo_question = """
Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.

The overall run time complexity should be O(log (m+n)).

 

Example 1:

Input: nums1 = [1,3], nums2 = [2]
Output: 2.00000
Explanation: merged array = [1,2,3] and median is 2.

Example 2:

Input: nums1 = [1,2], nums2 = [3,4]
Output: 2.50000
Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.

 

Constraints:

    nums1.length == m
    nums2.length == n
    0 <= m <= 1000
    0 <= n <= 1000
    1 <= m + n <= 2000
    -106 <= nums1[i], nums2[i] <= 106

"""

code_struct = '''
class Solution(object):
    def findMedianSortedArrays(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        """
'''
# ---- Interactive Session ----
if __name__ == "__main__":

    # Initialize an empty state
    state = create_agent_state(context=algo_question, real_code_struct=code_struct) #context=f''

    # Initial full pipeline run
    state = app.invoke(state) 

    # Save graph diagram to folder
    save_run(state, app, run_name=save_path, save_path='outputs')

    print('\n\n\n\n======== RESULTS ========\n\n')

    print(f'Code Solution: {state['pseudocode']}\n')

    print(f'Proof of Correctness: {state['proof']}\n')

    print(f'Big-O Notation: {state['complexity']}\n')

    print(f'Real Python Solution: {state['real_code']}\n')