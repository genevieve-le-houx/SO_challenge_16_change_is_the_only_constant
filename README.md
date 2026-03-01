# Stackoverflow challenge #16: Change is the only constant

This is my submission to Stackoverflow challenge #16: Change is the only constant

https://stackoverflow.com/beta/challenges/79888254/challenge-16-change-is-the-only-constant

The goal is to find the smallest number of coins needed to reach a given total, given a set of available coins.

For example, with a set of ten 1, two 5 and one 10, 
the smallest number of coins to reach 23 is with one 10, two 5 and three 1. (10*1 + 5*2 + 1*3 = 23)  .
So the answer would be 6, because 6 coins are needed. 

The data is in the file ``Challenge16.txt``. There are 100 sets.
Each set have three parts:
- A list of available coin values (denomination)
- A list of the quantity of each coin
- The target to reach

The answer is the number of coins needed for each set to reach the target

# Approach
We build a list of coins combination possibilities. At the end, we choose the possibility with the smallest number of coins needed.

A possibility is built this way: at each step (a step is choosing a coin), the possibles coin is smallest or equal of the biggest coin we have chosen so far.
We assume if a higher coin was possible, we would have chosen it earlier). 
The chosen coin must also bring the total of the possibility smallest or equal to the target and must still be available. 

So taking the given example, we would proceed this way

- When we start, we have all the coins possibilities, so 10, 5 or 1
- If we take the 10, we can now continue with a 10, a 5 or a 1. If we took the 5, we can continue with a 5 or a 1. If we took the 1, we can only continue with a 1

We continue iteratively to build all the possibilities. We then evaluate the possibilities to find the smallest number of coins needed.

# Execution
My code was done using Python 3.14.2. To execute, simply run main.py. No librairies needed.