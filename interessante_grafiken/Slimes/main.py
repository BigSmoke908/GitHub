from numba import jit, cuda
import numpy as np
# to measure exec time
from timeit import default_timer as timer


# normal function to run on cpu
def func(a):
    for i in range(10000000):
        a[i] += 1

    # function optimized to run on gpu


@jit(target="cuda")
def func2(a):
    for i in range(10000000):
        a[i] += 1


if __name__ == "__main__":
    n = 10000000
    a = np.ones(n, dtype=np.float64)
    b = np.ones(n, dtype=np.float32)

    start = timer()
    func(a)
    print("without GPU:", timer() - start)

    start = timer()
    func2(a)
    print("with GPU:", timer() - start)

# okay, so i found this video (https://www.youtube.com/watch?v=X-iSQQgOd1A), about these really cool looking slimes and i want to try out to do something similar myself with python. However, this will probably take a lot of compute power, so i decide to try out gpu processing for this. The problem is, that i have not really been able to find that good of a tutorial yet, is there any anyone can recommend? I dont need like every tiny little detail in the tutorial, but same basics, that work would be cool. I have found this article about it, together with jit as another optimization (https://www.geeksforgeeks.org/running-python-script-on-gpu/), but running the code with all libraries installed just gives a really long error message (i can send it, if you want it)
