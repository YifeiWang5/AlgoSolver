# Proving Algorithm Correctness: Induction & Contradiction

This document provides robust examples of proving algorithm correctness using **mathematical induction**, **contradiction**, and a hybrid of both.  

---

## 🔹 1. Proof by Mathematical Induction: Recursive Sum

**Algorithm:**  
```python
def sum_n(n):
    if n == 0:
        return 0
    return n + sum_n(n - 1)
```

**Claim:** `sum_n(n)` returns  
\[ 0 + 1 + 2 + ... + n = \frac{n(n+1)}{2} \]

**Proof by Induction on n:**

- **Base Case (n = 0):**  
  `sum_n(0) = 0`, and formula gives \(\frac{0(0+1)}{2} = 0\). ✅ Holds.

- **Inductive Hypothesis:**  
  Assume for some \(k \geq 0\),  
  \[ \texttt{sum\_n}(k) = \frac{k(k+1)}{2}. \]

- **Inductive Step (n = k+1):**  
  \[ \texttt{sum\_n}(k+1) = (k+1) + \texttt{sum\_n}(k). \]  
  By hypothesis,  
  \[ = (k+1) + \frac{k(k+1)}{2} = \frac{(k+1)(k+2)}{2}. \]  
  ✅ Matches the closed form.

- **Conclusion:** By induction, algorithm is correct for all \(n \geq 0\).

---

## 🔹 2. Proof by Contradiction: Linear Search Termination

**Algorithm:**  
```python
def linear_search(arr, x):
    for i in range(len(arr)):
        if arr[i] == x:
            return i
    return -1
```

**Claim:** The algorithm always terminates (no infinite loop).

**Proof (by contradiction):**

1. Assume the algorithm **does not terminate** for some input.  
   That means the `for` loop runs infinitely.

2. But in Python (or pseudocode), the loop runs exactly `len(arr)` iterations, which is **finite**.  

3. Contradiction: a finite loop cannot run infinitely.  

4. Therefore, the assumption is false, and the algorithm must always terminate.

---

## 🔹 3. Hybrid Proof (Induction + Contradiction): Binary Search

**Algorithm Idea:**  
Given a sorted array `A` and target `x`, binary search either finds `x` or concludes it is not present.  

**Claim:** Binary search correctly returns the index of `x` if it exists, otherwise reports "not found."

**Proof by Induction (on search interval size):**

- **Base Case (interval size = 1):**  
  If the interval has one element, the algorithm checks it directly. ✅ Correct.

- **Inductive Hypothesis:**  
  Assume binary search works correctly for any interval of size \(k\).

- **Inductive Step (interval size = k+1):**  
  Binary search compares `x` with the middle element:
  - If equal → correct answer immediately.  
  - If smaller → search left half (size ≤ k). By hypothesis, this is correct.  
  - If larger → search right half (size ≤ k). By hypothesis, this is correct.  

  Thus, correctness holds for size \(k+1\).

- **Conclusion:** By induction, binary search is correct for all intervals.

**Termination Proof by Contradiction:**  
Suppose binary search does not terminate. Then the search interval never decreases.  
But at each step, the algorithm halves the interval.  
A sequence of halvings cannot remain infinite. Contradiction. ✅

---

# 📌 Proof Template for Algorithm Correctness

You can adapt this template for other algorithms:

### Induction Proof Template
1. **Base Case:** Verify correctness for smallest input (e.g., n=0, n=1).  
2. **Inductive Hypothesis:** Assume algorithm works for input size `k`.  
3. **Inductive Step:** Show correctness for input size `k+1` (or recursive expansion).  
4. **Conclusion:** By induction, algorithm is correct for all inputs.

### Contradiction Proof Template
1. **Assume the opposite** of what you want to prove (e.g., algorithm doesn’t terminate, returns incorrect value).  
2. **Analyze algorithm behavior** step by step.  
3. **Show contradiction** with known facts (e.g., finite loop length, monotonic shrinking).  
4. **Conclusion:** Original claim holds true.
