import numpy as np

def obj(p_s, p_m):
    s = 0
    for i in range(len(p_s)):
        s += np.linalg.norm(p_s[i] - p_m[i]) ** 2
    return s

p_s = np.array([[1,5],
                [3,10],
                [5,10]])

p_om = np.array([[-2,-5],
                [0,0],
                [2,0]])

p_o = np.array([[0,0],
                [3,10],
                [6,12]])

for p in p_o:
    print(p)
    print(obj(p_s, p_om + p))

