try:
   import numpypy as np    # for compatibility with numpy in pypy
except:
   import numpy as np      # if using numpy in cpython

def TDMA(a, b, c, d):
    n = len(a)
    ac, bc, cc, dc = map(np.array, (a, b, c, d))
    xc = []
    for j in range(2, n):
        if(bc[j - 1] == 0):
            ier = 1
            return
        ac[j] = ac[j]/bc[j-1]
        bc[j] = bc[j] - ac[j]*cc[j-1]
    if(b[n-1] == 0):
        ier = 1
        return
    for j in range(2, n):
        dc[j] = dc[j] - ac[j]*dc[j-1]
    dc[n-1] = dc[n-1]/bc[n-1]
    for j in range(n-2, -1, -1):
        dc[j] = (dc[j] - cc[j]*dc[j+1])/bc[j]
    return dc

# small test. x = (1,2,3)
if __name__ == '__main__':
    a = [3,3,7]
    b = [2,1,6,8]
    c = [6,5,8,9,96,3,0,5,2]
    f = [10,16,30,8,0,9,4,3,1,7,8,1]
    print(TDMA(a,b,c,f))